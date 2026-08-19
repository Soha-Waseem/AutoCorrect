import re
from collections import Counter
from datasets import load_dataset
import streamlit as st

@st.cache_data
def load_data():
    """
    Loads Wikitext for a robust vocabulary and injects common contractions.
    Cached to prevent slow reloads on every Streamlit interaction.
    """
    word_counts = Counter()
    
    # Add common contractions that datasets often tokenize weirdly
    common_contractions = [
        "don't", "can't", "won't", "isn't", "aren't", "wasn't", "weren't",
        "hasn't", "haven't", "hadn't", "doesn't", "didn't", "couldn't",
        "shouldn't", "wouldn't", "mightn't", "mustn't", "it's", "he's",
        "she's", "that's", "who's", "what's", "where's", "there's",
        "i'm", "i've", "you've", "we've", "they've", "i'd", "you'd",
        "he'd", "she'd", "we'd", "they'd", "i'll", "you'll", "he'll",
        "she'll", "we'll", "they'll"
    ]
    for c in common_contractions:
        word_counts[c] += 10000

    # Load Wikitext-2 for a robust, dynamic vocabulary (~2M tokens)
    try:
        wikitext = load_dataset("wikitext", "wikitext-2-raw-v1", split="train")
        for item in wikitext:
            if item["text"].strip():
                # Extract words, allowing apostrophes for contractions (e.g., don't, can't)
                words = re.findall(r"\b[a-zA-Z']+\b", item["text"].lower())
                word_counts.update(words)
    except Exception as e:
        print(f"Error loading wikitext: {e}")

    # Explicitly block common contraction typos from being treated as valid words
    typo_blacklist = {
        "dont", "cant", "isnt", "arent", "wasnt", "werent", 
        "hasnt", "havent", "hadnt", "doesnt", "didnt", 
        "couldnt", "shouldnt", "wouldnt", "mustnt",
        "ive", "youve", "weve", "theyve", "youd", 
        "hed", "shed", "theyd", "youll", "theyll"
    }

    # Filter out rare words (< 3 occurrences) and blacklisted typos
    vocab = set(
        w for w, count in word_counts.items() 
        if count >= 3 and w not in typo_blacklist
    )
    
    return vocab, word_counts



