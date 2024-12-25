# OCR.py

import base64
from PIL import Image, ImageOps
import pytesseract
import io
import os
import time
import numpy as np
import json
from difflib import get_close_matches

def load_word_map():
    """Load the word map from JSON file"""
    try:
        with open('word-map.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement du word-map.json: {e}")
        return {}

def find_closest_match(word, word_map):
    """
    Find the closest matching word from the word map.
    
    Args:
        word (str): The word to match
        word_map (dict): Dictionary containing valid words
    
    Returns:
        str: The closest matching word from the word map
    """
    if not word:
        return ""
    
    cheat_sheet = {'rtp':'ftp', 'enu': 'gnu', 'urTL': 'url', 'spu': 'gpu', 'Tile': 'file', 'voLa': 'load', 'into': 'info', 'YASS': 'pass', 'Tast' : 'fast'}
    
    if word in cheat_sheet.keys():
        print(f"Mot original: '{word}' -> A utilisé la cheat sheet: '{cheat_sheet[word]}'")
        return cheat_sheet[word]
        
    # Get all words from the word map
    valid_words = list(word_map.keys())
    
    # Find closest matches
    matches = get_close_matches(word.lower(), valid_words, n=1, cutoff=0.6)
    
    if matches:
        closest_match = matches[0]
        print(f"Mot original: '{word}' -> Correspondance la plus proche: '{closest_match}'")
        return closest_match
    
    print(f"Aucune correspondance trouvée pour: '{word}'")
    return word

def extract_text_from_base64_image(base64_string):
    """
    Extracts text from a Base64-encoded image using OCR and finds the closest match in word-map.
    
    Args:
        base64_string (str): The Base64-encoded string of the image.
    
    Returns:
        str: The matched word from word-map
    """
    try:
        # Load word map
        word_map = load_word_map()
        if not word_map:
            return ""

        # Vérifier si la chaîne base64 est une URI de données
        if base64_string.startswith("data:image"):
            base64_data = base64_string.split(",")[1]
        else:
            base64_data = base64_string

        # Décoder la chaîne Base64 en octets
        image_data = base64.b64decode(base64_data)
        
        # Ouvrir l'image avec PIL
        image = Image.open(io.BytesIO(image_data))
        
        # Effectuer l'OCR avec pytesseract
        custom_config = '--psm 6 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        extracted_text = pytesseract.image_to_string(image, config=custom_config)
        
        # Nettoyer le texte extrait
        extracted_text = extracted_text.strip()
        print(f"Texte extrait par OCR: '{extracted_text}'")
        
        # Trouver la correspondance la plus proche dans word-map
        matched_word = find_closest_match(extracted_text, word_map)
        
        return matched_word
    except Exception as e:
        print(f"Erreur dans le module OCR: {e}")
        return ""

if __name__ == "__main__":
    # Test with a sample base64 image
    extract_text_from_base64_image("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
