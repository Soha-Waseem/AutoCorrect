# Autocorrect (An Intelligent Autocorrect Tool)

## Overview

Autocorrect is a hybrid NLP-based text correction system developed in Python that combines a custom rule-based spelling correction engine with a transformer-based grammar correction model. The system performs real-time spelling and grammar correction through a two-stage processing pipeline.

---

## Features

* Custom spell correction engine built from scratch
* Hybrid vocabulary construction using Wikitext-2 and wordfreq
* Damerau–Levenshtein edit distance implementation
* Candidate filtering and optimization for faster correction
* T5 transformer-based grammar correction
* Hallucination guard for output reliability
* Interactive Streamlit user interface
* End-to-end text correction pipeline

---

## How It Works

Autocorrect Pro uses a two-stage NLP pipeline:

### 1. Spelling Correction (Rule-Based Engine)

The input text is first tokenized into individual words. Each word is checked against a custom-built vocabulary created from Wikitext-2 and wordfreq datasets.

If a word is not found in the vocabulary:

* Candidate words are generated from the vocabulary
* Damerau–Levenshtein edit distance is computed to measure similarity
* Candidates are filtered using length and character-based heuristics
* Final correction is selected using a combined score of edit distance and word frequency

This stage fixes basic spelling errors like *“recieved → received”* or *“emial → email”*.

---

### 2. Grammar Correction (Transformer Model)

The corrected sentence is passed to a pretrained T5 transformer model with a “grammar:” prefix. The model uses beam search decoding to generate grammatically correct output.

A hallucination guard is applied to ensure reliability:

* Rejects outputs that are overly long compared to input
* Rejects outputs with low word overlap with original text

If the model output is unreliable, the system falls back to the spelling-corrected version.

---

### 3. Final Output

The final output is a clean sentence with corrected spelling and grammar, displayed in a Streamlit interface showing both correction stages separately.

---

## Tech Stack

**Languages**

* Python

**Libraries & Frameworks**

* Streamlit
* PyTorch
* Transformers
* Hugging Face Datasets
* wordfreq

**NLP Concepts**

* Tokenization
* Vocabulary Construction
* Edit Distance
* Dynamic Programming
* Beam Search
* Sequence-to-Sequence Models

---

## System Workflow

```text
User Input
     ↓
Rule-Based Spell Correction
     ↓
Vocabulary Lookup
     ↓
Candidate Generation
     ↓
Damerau–Levenshtein Matching
     ↓
Transformer-Based Grammar Correction (T5)
     ↓
Hallucination Validation
     ↓
Final Corrected Output
```

---

## Project Structure

```text
Autocorrect-Pro/
│
├── gui.py
├── nlp.py
├── model.py
├── dataset_loader.py
├── requirements.txt
└── README.md
```
---

## Installation

Clone repository:

```bash
git clone https://github.com/yourusername/Autocorrect-Pro.git
cd Autocorrect-Pro
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
streamlit run gui.py
```
