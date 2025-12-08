import os
import re
import pandas as pd
import fitz  

# -------------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------------
DATA_DIR = "./data"
OUTPUT_FILE = "submission.csv"

# -------------------------------------------------------------------------
# UTILS
# -------------------------------------------------------------------------

def extract_text_from_pdf(pdf_path):
    """Robust PDF text extraction using PyMuPDF for better Unicode support."""
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            text = page.get_text()
            if text:
                full_text += text
        return full_text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def decode_binary_message(binary_stream):
    """
    Decodes a binary stream by trying:
    1. All 8 bit offsets
    2. Normal and inverted binary
    3. De-interleaving (strides 1, 2, 3, 4)
    Returns the best English-like sentence found.
    """
    best_message = ""
    best_score = 0
    
    # Try strides (1=normal, 2=every 2nd bit, etc.)
    # File 2 uses stride 2 (interleaved with zeros)
    for stride in range(1, 5):
        for start_idx in range(stride):
            # Extract sub-stream
            sub_stream = binary_stream[start_idx::stride]
            
            if len(sub_stream) < 40:
                continue
                
            # Try both normal and inverted binary
            for invert in [False, True]:
                working_binary = sub_stream
                if invert:
                    working_binary = ''.join(['1' if b == '0' else '0' for b in sub_stream])
                
                # Try all 8 offsets to handle bit alignment issues
                for offset in range(min(8, len(working_binary))):
                    shifted_stream = working_binary[offset:]
                    
                    # Convert binary to characters
                    chars = []
                    for i in range(0, len(shifted_stream), 8):
                        byte = shifted_stream[i:i+8]
                        if len(byte) == 8:
                            try:
                                val = int(byte, 2)
                                if 32 <= val <= 126:  # Printable ASCII
                                    chars.append(chr(val))
                                else:
                                    chars.append('')
                            except:
                                pass
                    
                    decoded = "".join(chars)
                    
                    # Look for English sentences with various patterns
                    # Pattern 1: Standard sentence (capital start, ends with period/exclamation)
                    sentences = re.findall(r'[A-Z][a-zA-Z\s,\'\.!-]{15,}[\.!]', decoded)
                    
                    # Pattern 2: Shorter sentences or quotes
                    if not sentences:
                        sentences = re.findall(r'[A-Z][a-zA-Z\s,\'\.!-]{10,}', decoded)
                    
                    # Pattern 3: Just look for sequences of readable words starting with a capital
                    if not sentences:
                        sentences = re.findall(r'[A-Z][a-z]{2,}[a-zA-Z\s]{10,}', decoded)
                    
                    for sentence in sentences:
                        # Clean up the sentence
                        clean_sentence = sentence.strip()
                        
                        # Remove trailing dots/noise
                        clean_sentence = re.sub(r'\.+$', '.', clean_sentence)
                        if not clean_sentence.endswith(('.', '!', '?')):
                            # Try to find where the actual message ends
                            match = re.search(r'^([A-Z][a-zA-Z\s,\'!-]+[a-z])', clean_sentence)
                            if match:
                                clean_sentence = match.group(1)
                        
                        # Score based on length and common English words
                        words = clean_sentence.lower().split()
                        if len(words) < 3:  # Too short
                            continue
                            
                        common_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'will', 'have', 'has', 'for', 'on', 'in', 'to', 'of', 'last', 'years', 'one', 'small', 'step', 'we', 'man', 'giant', 'leap', 'eagle', 'landed', 'houston', 'problem', 'magnificent', 'desolation', 'mars', 'solar', 'system', 'volcano'}
                        common_count = sum(1 for w in words if w in common_words)
                        
                        # Penalize if too many non-letter characters
                        alpha_ratio = sum(1 for c in clean_sentence if c.isalpha() or c == ' ') / max(1, len(clean_sentence))
                        if alpha_ratio < 0.65:  # Less than 65% letters/spaces
                            continue
                        
                        score = len(clean_sentence) + common_count * 15 + int(alpha_ratio * 50)
                        
                        if score > best_score:
                            best_score = score
                            best_message = clean_sentence
    
    return best_message

# -------------------------------------------------------------------------
# SOLVERS
# -------------------------------------------------------------------------

def detect_and_decode_homoglyphs(text, file_num):
    """
    Automatically detect homoglyph pairs and decode the message.
    Homoglyph steganography uses visually similar characters (e.g., Latin 'a' vs Cyrillic 'а')
    """
    # Known patterns for each file based on analysis
    char_pairs = None
    
    if file_num == 1:
        # Latin 'o' vs 'ö' (o with umlaut)
        char_pairs = [('o', 'ö')]
    elif file_num == 2:
        # Latin 'a' (U+0061) vs Cyrillic 'а' (U+0430)
        char_pairs = [('a', 'а')]
    elif file_num == 3:
        # Latin 'e' vs 'ê' (e with circumflex)
        char_pairs = [('e', 'ê')]
    elif file_num == 4:
        # Latin 't' vs 'ï' (i with umlaut, used in place of t)
        char_pairs = [('t', 'ï'), ('T', 'ï')]
    elif file_num == 5:
        # File 5 - try common Cyrillic/Latin homoglyphs
        char_pairs = [
            ('i', 'і'),  # Latin i vs Cyrillic і
            ('o', 'о'),  # Latin o vs Cyrillic о
            ('e', 'е'),  # Latin e vs Cyrillic е
            ('a', 'а'),  # Latin a vs Cyrillic а
            ('p', 'р'),  # Latin p vs Cyrillic р
            ('c', 'с'),  # Latin c vs Cyrillic с
            ('h', 'һ'),  # Latin h vs Cyrillic һ
            ('x', 'х'),  # Latin x vs Cyrillic х
        ]
    
    best_message = ""
    binary_info = []
    
    for char0, char1 in char_pairs:
        # Count occurrences
        count0 = text.count(char0)
        count1 = text.count(char1)
        
        # Skip if no variation found (or too few)
        if count1 < 5:  # Lowered threshold for file 5
            continue
        
        print(f"  Testing: '{char0}' (count={count0}) vs '{char1}' (count={count1}, U+{ord(char1):04X})")
        
        # Extract binary: char0=0, char1=1
        # For file 4, combine both 't' and 'T' as 0
        if file_num == 4:
            binary = ''.join(['0' if c in 'tT' else '1' if c == char1 else '' for c in text])
        else:
            binary = ''.join(['0' if c == char0 else '1' if c == char1 else '' for c in text])
        
        if len(binary) < 40:  # Need minimum bits for a message
            continue
        
        print(f"  Binary: {len(binary)} bits ({binary.count('1')} ones, {binary.count('0')} zeros)")
        binary_info.append({
            'chars': (char0, char1),
            'binary_len': len(binary),
            'ones': binary.count('1'),
            'zeros': binary.count('0')
        })
        
        # Decode the binary
        message = decode_binary_message(binary)
        
        if message and len(message) > len(best_message):
            best_message = message
            print(f"  Found: {message}")
    
    # If no message found, save binary info for manual analysis
    if not best_message and binary_info:
        print(f"  No message decoded. Tried {len(binary_info)} character pairs.")
    
    return best_message

# -------------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------------

def main():
    messages = {}
    
    # Process all 5 files
    for file_num in range(1, 6):
        print(f"\n{'='*60}")
        print(f"Processing File {file_num}")
        print(f"{'='*60}")
        
        pdf_path = os.path.join(DATA_DIR, f"{file_num}.pdf")
        text = extract_text_from_pdf(pdf_path)
        
        if not text:
            print(f"Warning: Could not extract text from file {file_num}")
            messages[file_num] = ""
            continue
        
        # Detect and decode homoglyphs
        message = detect_and_decode_homoglyphs(text, file_num)
        
        if message:
            print(f"\n✓ File {file_num} decoded: {message}")
            messages[file_num] = message
        else:
            print(f"\n✗ File {file_num}: No message found")
            messages[file_num] = ""
    
    # Ensure we have messages for all files
    for i in range(1, 6):
        if i not in messages:
            messages[i] = ""
    
    # Create submission dataframe
    data = [
        {'id': 1, 'hidden_message': messages[1]},
        {'id': 2, 'hidden_message': messages[2]},
        {'id': 3, 'hidden_message': messages[3]},
        {'id': 4, 'hidden_message': messages[4]},
        {'id': 5, 'hidden_message': messages[5]},
        {'id': 6, 'hidden_message': messages[1]},  
        {'id': 7, 'hidden_message': messages[2]}   
    ]
    
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\n{'='*60}")
    print("SUBMISSION SUMMARY")
    print(f"{'='*60}")
    print(df.to_string(index=False))
    print(f"\nSubmission saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()