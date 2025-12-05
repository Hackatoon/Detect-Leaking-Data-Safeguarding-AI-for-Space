# ESA Hidden Message Detector

A comprehensive solution for the "Detect Leaking Data" Kaggle hackathon challenge focused on finding hidden messages in modified PDF documents.

## Overview

This solution implements multiple steganographic analysis techniques to detect hidden messages in PDF documents that have been modified using LLMs. The goal is to find text messages hidden within astronomy articles from "The Messenger" journal.

## Features

### Basic Detection Methods
- **Acrostic Analysis**: Extract first letters of words, sentences, and lines
- **Nth Character Extraction**: Extract every Nth character with various intervals
- **Positional Encoding**: Analyze last letters, capitals, word lengths
- **Pattern Recognition**: Number encoding, punctuation patterns
- **Keyword-Based**: Extract characters following astronomy-related keywords

### Advanced Steganography Techniques
- **Whitespace Analysis**: Detect binary encoding in trailing spaces and spacing patterns
- **Frequency Analysis**: Identify character frequency anomalies
- **Linguistic Patterns**: Sentence length encoding, word position analysis
- **Mathematical Sequences**: Fibonacci and prime number position extraction
- **Caesar Cipher Variants**: Apply different shifts to potential messages

### Message Validation
- English-like characteristics scoring
- Vowel ratio analysis
- Common word detection
- Character diversity assessment
- Space/astronomy keyword relevance
- Comprehensive scoring system

## Installation

```bash
# Install required packages
pip install -r requirements.txt

# Download NLTK data (first time only)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Usage

### Quick Start
```bash
# Run the comprehensive analysis
python main.py
```

### Individual Components
```bash
# Basic analysis only
python hidden_message_detector.py

# Test advanced techniques
python advanced_analysis.py
```

## File Structure

```
├── main.py                     # Main comprehensive detector
├── hidden_message_detector.py  # Basic steganography detection
├── advanced_analysis.py        # Advanced techniques and validation
├── requirements.txt            # Python dependencies
├── data/                       # PDF files (1.pdf, 2.pdf, ..., 5.pdf)
└── outputs/                    # Generated results
    ├── submission.csv          # Kaggle submission file
    ├── comprehensive_analysis.json
    └── document_analysis.json
```

## Output Format

The solution generates a CSV file in the required Kaggle format:
```csv
id,hidden_message
1,FOUND MESSAGE 1
2,FOUND MESSAGE 2
3,FOUND MESSAGE 3
4,FOUND MESSAGE 4
5,FOUND MESSAGE 5
6,FOUND MESSAGE 1
7,FOUND MESSAGE 2
```

## Algorithm Details

### Detection Pipeline
1. **PDF Text Extraction**: Uses PyMuPDF and pdfplumber for robust text extraction
2. **Multi-Method Analysis**: Applies 15+ different steganographic detection techniques
3. **Message Scoring**: Each potential message receives a comprehensive score
4. **Validation**: Messages are validated for English-like characteristics
5. **Ranking**: All messages are ranked by score and validity
6. **Selection**: Best message per document is selected for submission

### Scoring Criteria
- Message length (longer = better, up to a point)
- English vowel ratio (20-60% is ideal)
- Presence of common English words
- Character diversity (avoid excessive repetition)
- Space/astronomy keyword relevance
- Pattern consistency

## Key Techniques for Competition

### Difficulty Progression
The solution handles increasing difficulty across files 1-5:
- **Files 1-2**: Simple acrostic and positional methods
- **Files 3-4**: Advanced mathematical sequences and linguistic patterns  
- **File 5**: Complex whitespace encoding and cipher variations

### Space Domain Optimization
- Prioritizes astronomy/space-related keywords
- Uses ESA, telescope, mission, orbit, etc. as anchor points
- Applies domain knowledge for pattern recognition

## Performance Notes

- Processes all 5 documents in ~30-60 seconds
- Generates 20+ potential messages per document
- Comprehensive scoring and validation system
- Handles various PDF formatting issues robustly

## Example Output

```
File 1: 'DATASECURITY' (method: acrostic_sentences, score: 8.2) ✓
File 2: 'HIDDEN' (method: capital_letters, score: 6.5) ✓
File 3: 'MISSION' (method: every_7th_char, score: 7.1) ✓
File 4: 'TELESCOPE' (method: fibonacci_positions, score: 9.3) ✓
File 5: 'SPACEDATA' (method: whitespace_binary, score: 8.8) ✓
```

## Competition Strategy

1. **Multi-Method Approach**: Uses 15+ different extraction techniques
2. **Robust Validation**: Ensures messages are meaningful
3. **Difficulty Scaling**: Adapts to increasing complexity
4. **Domain Focus**: Leverages space/astronomy context
5. **Quality over Quantity**: Prioritizes best-scored message per file

The solution is designed to maximize success across all difficulty levels while maintaining robustness and avoiding false positives.