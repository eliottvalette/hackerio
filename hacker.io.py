# hacker_io_bot.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from OCR import extract_text_from_base64_image

def save_word_pair(img_src, extracted_text):
    try:
        # Read the existing JSON file
        file_path = "saved-words.json"
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        # Add the new word pair
        data[img_src] = extracted_text

        # Write back the updated JSON
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving word pair: {e}")

def load_saved_words():
    """Load the saved words from JSON file"""
    try:
        with open('saved-words.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement du saved-words.json: {e}")
        return {}

def open_hacker_io():
    # Initialiser le WebDriver Chrome (assurez-vous que chromedriver est dans le PATH)
    driver = webdriver.Chrome()
    
    # Créer un objet WebDriverWait avec un délai d'attente de 15 secondes
    wait = WebDriverWait(driver, 15)

    # Naviguer vers le site cible
    driver.get("https://s0urce.io/")

    saved_words = load_saved_words()
    try:
        # ------------LANCEMENT DU JEU------------
        # Attendre que le champ de saisie soit cliquable et saisir le nom
        name_input_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="input"]')))
        name_input_field.send_keys("Los Valettos")
        print("Nom saisi avec succès.")

        # Attendre que le bouton Play soit cliquable et cliquer dessus
        play_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.grey.svelte-ec9kqa")))
        play_button.click()
        print("Bouton Play cliqué.")

        time.sleep(1)

        # ------------CLIQUE SUR LE DIV "TARGET LIST"------------
        target_list_xpath = "//div[text()='Target List']"
        target_list_div = wait.until(EC.element_to_be_clickable((By.XPATH, target_list_xpath)))
        target_list_div.click()
        print("Div 'Target List' cliqué.")

        time.sleep(1)

        # ------------CLIQUE SUR LE DIV "PLAYER HACKABLE"------------
        real_target_list_div = wait.until(EC.element_to_be_clickable((By.ID, 'list')))
        first_child_div = real_target_list_div.find_element(By.XPATH, "./div[1]")
        first_child_div.click()
        print("Div 'Player Hackable' cliqué.")

        hack_button_xpath = "//button[text()='Hack']"
        hack_button = wait.until(EC.element_to_be_clickable((By.XPATH, hack_button_xpath)))
        hack_button.click()
        print("Bouton 'Hack' cliqué.")

        hack_port_button_xpath = "//button[contains(text(), 'Port ')]"
        hack_port_button = wait.until(EC.element_to_be_clickable((By.XPATH, hack_port_button_xpath)))
        hack_port_button.click()
        print("Bouton 'Port 21' cliqué.")

        time.sleep(1)

        fails = 0
        while True :
            try :
                tries_left = "//div[text()='Tries: ']"
                tries_left_div = wait.until(EC.presence_of_element_located((By.XPATH, tries_left)))
                old_tries = int(tries_left_div.text[-1])

                # ------------START HACKING------------
                word_to_type_div = wait.until(EC.presence_of_element_located((By.ID, 'word-to-type')))
                word_img = word_to_type_div.find_element(By.TAG_NAME, "img")
                img_src = word_img.get_attribute("src")

                if img_src in saved_words.keys():
                    print(f"Mot déjà sauvegardé ///////////: {saved_words[img_src]}")
                    extracted_text = saved_words[img_src]
                else:
                    # Extract text using the OCR module
                    extracted_text = extract_text_from_base64_image(img_src).lower()
                    print(f"Extracted Text: {extracted_text}")

                # ------------TAPER LE MOT EXTRAI--------
                # Remplacez le sélecteur ci-dessous par celui de votre champ de saisie cible
                target_input_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="input"]')))
                target_input_field.send_keys(extracted_text)

                # ------------CLIQUE SUR LE BOUTON "SUBMIT"------------
                submit_button_xpath = "//button[text()='Enter']"
                submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
                submit_button.click()

                time.sleep(1)
                tries_left_div = wait.until(EC.presence_of_element_located((By.XPATH, tries_left)))
                new_tries = int(tries_left_div.text[-1])

                if old_tries > new_tries :
                    print("##### FAILED #####")
                    fails+=1
                else :
                    print("##### SUCCESS #####")
                    # Save successful word recognition
                    save_word_pair(img_src, extracted_text)
                    
                if fails == 3 :
                    print('THE END')
                    break

                time.sleep(1)
            except Exception as e:
                print(f"Erreur lors du clic sur le bouton 'Enter': {e}")
                break

            time.sleep(1)

        # Optionnel : Attendre quelques secondes pour observer le résultat
        time.sleep(10)

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    
    finally:
        # Toujours fermer le navigateur après les opérations
        driver.quit()
        print("Navigateur fermé.")

if __name__ == "__main__":
    for i in range(10):
        open_hacker_io()
