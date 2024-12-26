# hacker_io_bot.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import os
import time
import random
import json
from OCR import extract_text_from_base64_image

load_dotenv()
phone = os.getenv("PHONE")
password = os.getenv("PASSWORD")
class HackerIOBot:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.saved_words = self.load_saved_words()
        self.saved_words_OCR = self.load_saved_words_OCR()
        self.fails = 0

    def setup_driver(self):
        """Initialize and configure the Chrome WebDriver"""
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 2)
        self.driver.set_window_size(820, 1080)
        self.driver.get("https://s0urce.io/")

    def load_saved_words(self):
        """Load previously saved word-image pairs"""
        try:
            with open('saved-words.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading saved-words.json: {e}")
            return {}

    def load_saved_words_OCR(self):
        """Load previously saved word-image pairs"""
        try:
            with open('word-map.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading word-map.json: {e}")
            return {}

    def save_word_pair(self, img_src, extracted_text):
        """Save successful word-image pairs"""
        try:
            self.saved_words[img_src] = extracted_text
            with open("saved-words.json", "w") as file:
                json.dump(self.saved_words, file, indent=4)
        except Exception as e:
            print(f"Error saving word pair: {e}")

    def save_word_pair_OCR(self, OCR_pred, extracted_text):
        """Save successful word-image pairs"""
        try:
            self.saved_words_OCR[OCR_pred] = extracted_text
            with open("word-map.json", "w") as file:
                json.dump(self.saved_words_OCR, file, indent=4)
        except Exception as e:
            print(f"Error saving word pair: {e}")

    def login(self, unknown=False):
        """Handle the login process"""
        if unknown:
            name_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="input"]')))
            name_input.send_keys("Los Valettos")
            
            play_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.grey.svelte-ec9kqa")))
            play_button.click()
        else :
            login_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "green")))
            login_button.click()

            auth_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/auth/twitter']")) )
            auth_link.click()

            time.sleep(3)

            phone_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="text"]')))
            phone_input.send_keys(phone)

            next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]")))
            next_button.click()

            time.sleep(1)

            password_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="password"]')))
            password_input.send_keys(password)

            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Log in']]")))
            login_button.click()

            time.sleep(3)

            auth_app_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Authorize app']]")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", auth_app_button)
            auth_app_button.click()

            time.sleep(3)

            play_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "green")))
            play_button.click()

            time.sleep(1)

    def select_target(self):
        """Select a target to hack"""
        try:
            # Wait for any existing windows to be closeable
            time.sleep(0.1)
            
            # Wait and click target list
            target_list = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Target List']")))
            self.driver.execute_script("arguments[0].click();", target_list)
            time.sleep(0.1)

            # Wait and click first target
            real_target_list = self.wait.until(EC.element_to_be_clickable((By.ID, 'list')))
            targets = real_target_list.find_elements(By.XPATH, "./div")
            random_target = random.choice(targets[:2] + targets[5:])
            self.driver.execute_script("arguments[0].click();", random_target)
            
        except Exception as e:
            print(f"Error selecting target: {e}")
            return

    def start_hack(self):
        """Initiate the hacking process"""
        try:
            time.sleep(0.1)
            # Check if hack button is clickable
            hack_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Hack']")))
            
            # Check if button has 'cantClick' class
            if 'cantClick' in hack_button.get_attribute("class"):
                print("Hack button is not clickable (timer active). Skipping...")
                return False
            
            hack_button.click()
            
            # Try to click port button
            port_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Port ')]")))
            port_button.click()
            time.sleep(0.1)
            return True
            
        except Exception as e:
            print(f"Error starting hack: {e}")
            return False

    def get_current_tries(self):
        """Get the current number of tries left"""
        tries_div = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Tries: ']")))
        return int(tries_div.text[-1])

    def process_word(self):
        """Process the word to be typed"""
        word_div = self.wait.until(EC.presence_of_element_located((By.ID, 'word-to-type')))
        word_img = word_div.find_element(By.TAG_NAME, "img")
        img_src = word_img.get_attribute("src")

        if img_src in self.saved_words:
            print(f"Using saved word: {self.saved_words[img_src]}")
            return img_src, self.saved_words[img_src], self.saved_words[img_src]
        
        text, OCR_result = extract_text_from_base64_image(img_src)
        print(f"Extracted text: {text}")
        return img_src, text, OCR_result

    def submit_word(self, word):
        """Submit the word and handle the result"""
        input_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="input"]')))
        input_field.send_keys(word)

        submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Enter']")))
        submit_button.click()
        time.sleep(0.1)

    def check_progress(self):
        """Check if hacking is complete"""
        print("Checking progress...")
        # Updated selector to match the correct class structure
        progress_bar = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'target-bar')))
        progress_div = progress_bar.find_element(By.CLASS_NAME, 'target-bar-progress')
        
        # Get the width style
        style = progress_div.get_attribute("style")        
        # Extract the percentage
        if style and "width" in style:
            progress = style.replace("width: ", "").replace("%;", "")
            return progress == "100"
        return False

    def take_all(self):
        """Take all the rewards"""
        try:
            take_all_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "green")))
            take_all_button.click()
            time.sleep(0.1)
        except Exception as e:
            pass

    def open_inventory(self):
        """Open the inventory"""
        try:
            # Wait for any existing windows to be closeable
            time.sleep(0.1)
            
            # Wait and click target list
            inventory_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Inventory']")))
            self.driver.execute_script("arguments[0].click();", inventory_button)
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Error selecting target: {e}")
            raise e
    
    def take_item(self):
        """Take an item using double-click and ensure it is processed correctly."""
        try:
            time.sleep(0.5)
            # Check if there are any items first
            items = self.driver.find_elements(By.CLASS_NAME, "name")
            if not items:
                print("No items found to take")
                return
                
            for item in items:
                try:
                    if not item.is_displayed():
                        continue
                        
                    print(f"Taking item: {item.text if item.text else 'Unnamed Item'}")
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", item)
                    actions = ActionChains(self.driver)
                    actions.double_click(item).perform()
                    time.sleep(0.1)
                except Exception as e:
                    print(f"Failed to take item: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error in take_item: {e}")
            # Don't raise the error, just log it
            return


    def close_window(self):
        """Close the hacking window with improved error handling"""
        try:
            # Wait for any animations to complete
            time.sleep(0.1)
            
            # Find all close buttons and try to close them
            close_buttons = self.driver.find_elements(By.CLASS_NAME, 'window-close')
            for button in close_buttons:
                try:
                    # Try multiple closing strategies
                    try:
                        button.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", button)
                except:
                    continue
            
            # If clicking didn't work, try escape key
            if len(close_buttons) > 0:
                from selenium.webdriver.common.keys import Keys
                webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                
        except Exception as e:
            print(f"Error closing window: {e}")
            # Final fallback - refresh the page
            try:
                self.driver.refresh()
                time.sleep(0.3)
            except:
                pass

    def hack_loop(self):
        """Main hacking loop"""
        self.fails = 0
        while True:
            try:
                old_tries = self.get_current_tries()
                img_src, word, OCR_result = self.process_word()
                self.submit_word(word)
                new_tries = self.get_current_tries()

                if old_tries > new_tries:
                    print("##### FAILED #####")
                    with open('failed-words.txt', 'a') as f:
                        f.write(f"{OCR_result} -- {word}\n")
                    self.fails += 1
                else:
                    print("##### SUCCESS #####")
                    self.save_word_pair(img_src, word)
                    self.save_word_pair_OCR(OCR_result, word)

                if self.fails == 3 :
                    print("##### THE END (LOST) #####")
                    self.close_window()
                    self.close_window()
                    break
                    
                if self.check_progress():
                    print("##### THE END (WON) #####")
                    self.close_window()
                    self.close_window()
                    break

                time.sleep(0.1)

            except Exception as e:
                print(f"Error in hack loop: {e}")
                break

    def run_interactive(self):
        """Interactive main method"""
        self.setup_driver()
        self.login()
        try:
            while True:
                command = input("\nCommands:\n"
                              "h - Start hack and loop\n"
                              "c - Close window\n"
                              "r - Take all rewards\n"
                              "a - Activate auto-bot\n"
                              "q - Quit\n"
                              "Enter command: ").lower()

                if command == 'h':
                    number_of_hacks = input("How many hacks to do? ")
                    for _ in range(int(number_of_hacks)):
                        if self.driver:
                            self.select_target()
                            if self.start_hack():  # Only continue if hack started successfully
                                self.hack_loop()
                                print("Hack complete")
                            else:
                                print("Skipping to next target...")
                                self.close_window()  # Close the target window
                        else:
                            print("Please setup first (s)")

                elif command == 'q':
                    if self.driver:
                        self.driver.quit()
                        print("Browser closed")
                    break

                elif command == 'c':
                    if self.driver:
                        self.close_window()
                        print("Window closed")
                    else:
                        print("Please setup first (s)")

                elif command == 'r':
                    if self.driver:
                        self.take_all()
                        self.open_inventory()
                        self.take_item()
                        print("All rewards taken")
                    else:
                        print("Please setup first (s)")
                
                elif command == 'a':
                    print("Auto-bot activated")
                    while True:
                        for _ in range(int(10)):
                            self.select_target()
                            if self.start_hack():
                                self.hack_loop()
                                print("Hack complete")
                            else:
                                print("Skipping to next target...")
                                self.close_window()
                        self.take_all()
                        self.open_inventory()
                        self.take_item()
                        self.close_window()
                        self.close_window()

                else:
                    print("Invalid command")

        except Exception as e:
            print(f"An error occurred: {e}")
            if self.driver:
                self.driver.quit()
                print("Browser closed due to error")

if __name__ == "__main__":
    bot = HackerIOBot()
    bot.run_interactive()
