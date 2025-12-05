# Solution Notes: Data Leakage Detection

## Overview
This solution implements a programmatic approach to detect hidden messages in PDF files using homoglyph steganography techniques.

## Approach

### 1. **PDF Text Extraction**
- Uses PyMuPDF (fitz) for better Unicode character handling
- Extracts all text while preserving special characters

### 2. **Homoglyph Detection**
Homoglyph steganography uses visually similar characters from different character sets:
- **File 1**: Latin 'o' (U+006F) vs 'ö' (U+00F6) - WORKING ✓
- **File 2**: Latin 'a' (U+0061) vs Cyrillic 'а' (U+0430) - In Progress
- **File 3**: Latin 'e' (U+0065) vs 'ê' (U+00EA) - In Progress  
- **File 4**: Latin 't' (U+0074) vs 'ï' (U+00EF) - In Progress
- **File 5**: Multiple Cyrillic/Latin pairs tested - In Progress

### 3. **Binary Extraction & Decoding**
- Extracts binary stream where normal char = '0', special char = '1'
- Tries all 8 bit offsets to handle alignment issues
- Tests both normal and inverted binary (swap 0s and 1s)
- Converts 8-bit chunks to ASCII characters
- Uses pattern matching to find English sentences

## Results

### File 1: **SUCCESS** ✓
- **Message**: "Apollo footprints will last a million years"
- **Method**: o/ö homoglyph encoding (Standard 8-bit ASCII)
- **Binary**: 802 bits (166 ones, 636 zeros)
- **Confidence**: 100% - Programmatically decoded

### File 2: **SUCCESS** ✓
- **Message**: "Mars has the tallest volcano in the Solar System"
- **Method**: a/а homoglyph encoding (Interleaved Binary)
  - The message is encoded in the **even bits** (indices 0, 2, 4...) of the binary stream.
  - The odd bits are all '0' (padding).
  - De-interleaving (taking every 2nd bit) reveals the standard 8-bit ASCII message.
- **Binary**: 771 bits (175 ones, 596 zeros)
- **Confidence**: 100% - Programmatically decoded

### File 3: **Unsolved**
- **Technique**: e/ê homoglyph substitution.
- **Analysis**: 83 'ê' characters found (2.5% density). Words containing 'ê' mostly start with 's'. Standard decoding failed.

### File 4: **Unsolved**
- **Technique**: t/ï homoglyph substitution.
- **Analysis**: 136 'ï' characters found (1.2% density). Words containing 'ï' mostly start with 'c'. Standard decoding failed.

### File 5: **Unsolved**
- **Status**: No clear homoglyph pattern identified yet.

## Technical Details

### Homoglyph Steganography
The technique embeds binary data by substituting visually similar characters:
- Each occurrence of the "normal" character represents bit '0'
- Each occurrence of the "special" character represents bit '1'
- The binary stream is then decoded as ASCII characters

### Challenges
- PDF extraction may normalize certain Unicode characters
- Bit alignment can vary
- Need to distinguish actual messages from noise
- Files 2-4 have very few '1' bits, suggesting alternative encoding methods

## Next Steps for Complete Solution

To improve detection of files 2-5:
1. Analyze word-level or sentence-level encoding
2. Check for positional steganography
3. Investigate spacing-based encoding
4. Consider semantic steganography techniques
5. Examine font or formatting variations

## Usage

```bash
python main.py
```

The script will:
1. Process all 5 PDF files
2. Detect homoglyph pairs automatically
3. Extract and decode binary messages
4. Generate `submission.csv` with results
