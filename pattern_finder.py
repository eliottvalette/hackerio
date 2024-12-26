import re
import json
from tqdm import tqdm
from collections import defaultdict

def find_unique_patterns(data):
    """
    Find unique patterns for each word based on the Base64 keys.
    
    Args:
        data (dict): Dictionary with Base64 keys as keys and associated words as values.
        
    Returns:
        dict: A dictionary where each word is mapped to a unique pattern, or None if no pattern is found.
    """
    # Group keys by associated word
    word_to_keys = defaultdict(list)
    for key, word in data.items():
        word_to_keys[word].append(key)
    
    # Find unique patterns for each word
    unique_patterns = {}
    
    for word, keys in tqdm(word_to_keys.items()):
        # Start with all potential substrings of the first key
        patterns = {key[i:j] for key in keys for i in range(len(key)) for j in range(i + 1, len(key) + 1)}
        
        # Retain only patterns present in all keys of this word
        for key in keys:
            patterns &= {key[i:j] for i in range(len(key)) for j in range(i + 1, len(key) + 1)}
        
        # Check uniqueness: Ensure no other word's keys contain these patterns
        found_unique = False
        for pattern in sorted(patterns, key=len, reverse=True):  # Sort by length for specificity
            is_unique = True
            for other_word, other_keys in word_to_keys.items():
                if other_word == word:
                    continue
                if any(pattern in other_key for other_key in other_keys):
                    is_unique = False
                    break
            if is_unique:
                unique_patterns[word] = pattern
                found_unique = True
                break
        
        # Fallback if no unique pattern found
        if not found_unique:
            unique_patterns[word] = None  # Or provide a default fallback pattern
            print(f"Warning: No unique pattern found for word '{word}'")

    return unique_patterns

if __name__ == "__main__":
    # Load data
    with open('saved-words.json', 'r') as f:
        base64_to_word = json.load(f)

    print(f"Total keys: {len(base64_to_word.keys())}")
    print(f"Unique keys: {len(set(base64_to_word.keys()))}")

    # Find patterns
    patterns = find_unique_patterns(base64_to_word)

    # Save the results or process further
    with open("patterns.json", "w") as outfile:
        json.dump(patterns, outfile, indent=4)
