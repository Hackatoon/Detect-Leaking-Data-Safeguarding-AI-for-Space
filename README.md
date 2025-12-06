# ESA Hidden Message Detector

A comprehensive solution for the "Detect Leaking Data" Kaggle hackathon challenge focused on finding hidden messages in modified PDF documents.

## Overview

This solution implements multiple steganographic analysis techniques to detect hidden messages in PDF documents that have been modified using LLMs. The goal is to find text messages hidden within astronomy articles from "The Messenger" journal.

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

## Usage

```bash
python main.py
```

