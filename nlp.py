import re
from dataset_loader import load_data

# Initialize vocabulary and word counts from dataset
VOCAB, WORD_COUNTS = load_data()


def clean_word(word):
    """Remove non-alphabetic characters (except apostrophes) and convert to lowercase."""
    return re.sub(r"[^a-zA-Z']", "", word).lower()

def edit_distance(s1, s2):
    """Damerau-Levenshtein Algorithm for word similarity matching (includes transpositions)."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # deletion
                dp[i][j - 1] + 1,      # insertion
                dp[i - 1][j - 1] + cost  # substitution
            )
            # Transposition check
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + cost)
    return dp[m][n]


def get_candidates(word, max_distance=2):
    """
    Selects potential correction candidates from vocabulary.
    Optimized to filter by length before computing Edit Distance.
    """
    candidates = []
    
    # If vocabulary is empty (e.g. dataset load error), return empty
    if not VOCAB:
        return []

    # Optimization: Only check words with similar length
    # This significantly speeds up the search compared to checking 100k+ words
    for vocab_word in VOCAB:
        if abs(len(vocab_word) - len(word)) > max_distance:
            continue
        
        # Another optimization: must share at least one character or be very short
        # (This is a heuristic to avoid full edit distance on very dissimilar words)
        if len(word) > 3 and not any(char in vocab_word for char in word[:2]):
            continue

        distance = edit_distance(word, vocab_word)
        if distance <= max_distance:
            candidates.append(vocab_word)
            
    return candidates

def correct_word(word):
    """Corrects a single word using rule-based approach."""
    cleaned = clean_word(word)
    if cleaned == "" or cleaned in VOCAB:
        return word

    # Try distance 1 first for speed and accuracy
    candidates = get_candidates(cleaned, max_distance=1)
    
    # If no distance 1, try distance 2
    if not candidates:
        candidates = get_candidates(cleaned, max_distance=2)

    if not candidates:
        return word

    # Frequency-based selection: select most frequent candidate from dataset
    best = max(candidates, key=lambda w: WORD_COUNTS.get(w, 0))

    # Preserve original capitalization
    if word[0].isupper():
        best = best.capitalize()
    return best

def spell_correct_sentence(sentence):
    """Corrects all words in a sentence."""
    # Split while preserving punctuation
    tokens = re.findall(r"[\w']+|[.,!?;]", sentence)
    corrected_tokens = []

    for token in tokens:
        if re.match(r"\w+", token):
            corrected_tokens.append(correct_word(token))
        else:
            corrected_tokens.append(token)

    # Join tokens, but handle punctuation spacing
    result = ""
    for i, token in enumerate(corrected_tokens):
        if i > 0 and re.match(r"\w+", token) and not re.match(r"[.,!?;]", corrected_tokens[i-1]):
            result += " " + token
        elif i > 0 and re.match(r"\w+", token):
             result += " " + token
        else:
            result += token
    
    return result.strip()
