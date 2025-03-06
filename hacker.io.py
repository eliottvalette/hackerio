# hacker_io.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from OCR import extract_text_from_base64_image
from dotenv import load_dotenv

import os
import time
import random
import json
import math

from time import sleep
import threading

load_dotenv()

username = os.getenv("USERNAME")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def input_with_timeout(prompt, timeout):
    user_input = [None]  # Use a mutable object to store the input

    def get_input():
        user_input[0] = input(prompt)

    # Start a thread to get input
    thread = threading.Thread(target=get_input)
    thread.start()
    thread.join(timeout)  # Wait for the thread to finish or timeout

    if thread.is_alive():
        # If the thread is still running, input timed out
        print("\nInput timed out!")
        return 'n'

    return user_input[0]

class HackerIOBot:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.saved_words_OCR = self.load_saved_words_OCR()
        self.fails = 0
        self.run_auto_bot = False
        self.auto_up = False

    def setup_driver(self):
        """Initialize and configure the Chrome WebDriver"""
        try:
            # Initialize Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Randomize window size slightly
            width = random.randint(1280, 1366)
            height = random.randint(768, 900)
            chrome_options.add_argument(f"--window-size={width},{height}")
            
            # Initialize Chrome driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 2)
            
            self.driver.get("https://s0urce.io/")
            
            # Get window dimensions
            self.width = self.driver.execute_script("return window.innerWidth;")
            self.height = self.driver.execute_script("return window.innerHeight;")

            time.sleep(3)
            
        except Exception as e:
            print(f"Error in setup: {e}")
            if self.driver:
                self.driver.quit()
            raise e

    def load_saved_words_OCR(self):
        """Load previously saved word-image pairs"""
        try:
            with open('word-map.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading word-map.json: {e}")
            return {}

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
        self.wait = WebDriverWait(self.driver, 5)
        if unknown:
            name_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="input"]')))
            # Random name with 7 letters
            name_input.send_keys("FullTryhard" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=7)))

            play_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.grey.svelte-ec9kqa")))
            play_button.click()
        else :
            try: 
                login_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "green")))
                login_button.click()

                auth_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/auth/twitter']")) )
                auth_link.click()

            except:
                pass

            time.sleep(1)
            
            try: 
                username_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="text"]')))
                username_input.send_keys(username)

                next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]")))
                next_button.click()
            except:
                pass

            try :
                email_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="text"]')))
                email_input.send_keys(email)

                next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]")))
                next_button.click()
            except :
                pass

            try : 
                password_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="password"]')))
                password_input.send_keys(password)

                login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Log in']]")))
                login_button.click()
            except :
                pass

            try:
                auth_app_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Authorize app']]")))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", auth_app_button)
                auth_app_button.click()
            except :
                pass
                
            time.sleep(1)

            self.close_window()

            try:
                play_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Play']]")))
                play_button.click()
            except :
                pass

        self.wait = WebDriverWait(self.driver, 2)
    
    def click_green_button(self):
        """Click the green button"""
        try:
            green_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "green")))
            green_button.click()
        except Exception as e:
            print(f"Error clicking green button: {e}")

    def refresh_and_relogin(self):
        """Refresh the page and relogin"""
        try:
            self.driver.refresh()
            time.sleep(3)
            try : 
                green_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "green")))
                green_button.click()
            except:
                self.login()
        except Exception as e:
            print(f"Error refreshing and relogging: {e}")

    def select_target(self):
        """Select a valid target to hack based on criteria (minimal wait)."""
        try:
            time.sleep(0.1)
            
            # Click target list
            target_list = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Target List']")))
            self.driver.execute_script("arguments[0].click();", target_list)
            time.sleep(0.1)
            
            # Locate targets
            real_target_list = self.wait.until(EC.presence_of_element_located((By.ID, 'list')))
            targets = real_target_list.find_elements(By.XPATH, "./div")

            valid_targets = []
            
            # Filter targets
            for target in targets:
                target_text = target.text.strip()
                if not target_text:
                    continue

                target_parts = target_text.split()
                
                # Check conditions
                has_level = target_parts[0].isdigit()
                lvl = int(target_parts[0]) if has_level else 0
                has_cooldown = any(part[:-1].isdigit() and part[-1] in ['m', 's'] for part in target_parts)
                is_vash = "Vash" in target_parts
                is_you = "(you)" in target_parts
                
                if has_level and not has_cooldown and not is_you and not is_vash and lvl < 45:
                    valid_targets.append(target)
            
            # Save targets for debugging
            with open('valid_targets.txt', 'w') as f:
                for t in valid_targets:
                    f.write(f"{t.text}\n")
            
            if valid_targets:
                selected_target = None
                def get_target_level(t):
                    parts = t.text.strip().split()
                    try:
                        return (0 if "NPC" in parts else 1, int(parts[0]))
                    except:
                        return (1, 999)
                
                valid_targets.sort(key=get_target_level)
                
                # If first is NPC, pick it, else random from the first 6
                if "NPC" in valid_targets[0].text:
                    selected_target = valid_targets[0]
                else:
                    selected_target = random.choice(valid_targets[:6])
            else:
                # If no valid targets, default to the first
                selected_target = targets[0]

            if selected_target:
                is_npc = "NPC" in selected_target.text
                self.driver.execute_script("arguments[0].click();", selected_target)
                print(f"Selected target: {selected_target.text}")
                time.sleep(0.1)
                return is_npc
            else:
                print("No valid targets found")
                return False
        except Exception as e:
            print(f"Error selecting target: {e}")
            self.close_window()

    def start_hack(self):
        """Initiate the hacking process"""
        try:
            time.sleep(0.1)  # Increased wait time
            
            # Find and click hack button
            hack_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Hack']")))
            
            if 'cantClick' in hack_button.get_attribute("class"):
                print("Hack button is not clickable (timer active). Skipping...")
                return False
            
            # Click hack button using JavaScript
            self.driver.execute_script("arguments[0].click();", hack_button)
            time.sleep(0.1)  # Wait for animation
            
            # Find and click port button
            try:
                port_button = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Port ')]")
                ))
                self.driver.execute_script("arguments[0].click();", port_button)
                time.sleep(0.1)
                
                # Verify hack window is open
                self.wait.until(EC.presence_of_element_located((By.ID, 'word-to-type')))
                return True
                
            except Exception as e:
                print(f"Error clicking port button: {e}")
                return False

        except Exception as e:
            print(f"Error starting hack: {e}")
            return False

    def get_current_tries(self):
        """Get the current number of tries left"""
        tries_div = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Tries: ']")))
        return int(tries_div.text[-1])

    def process_word(self):
        """Process the word to be typed"""
        try:
            # More specific and reliable selector based on the HTML structure
            word_div = self.wait.until(EC.presence_of_element_located((By.ID, 'word-to-type')))
            word_img = word_div.find_element(By.TAG_NAME, "img")
            img_src = word_img.get_attribute("src")
            
            # Enhanced error handling for OCR
            if not img_src:
                print("Warning: No image source found")
                return None, "", ""
                
            text, OCR_result = extract_text_from_base64_image(img_src)
            
            # Debug logging
            print(f"OCR Result: '{OCR_result}', Matched Word: '{text}'")
            
            return img_src, text, OCR_result
        except Exception as e:
            print(f"Error processing word: {e}")
            return None, "", ""

    def random_delay(self, min_delay=0.02, max_delay=0.1):
        """Add random delay between actions"""
        sleep(random.uniform(min_delay, max_delay))

    def submit_word(self, word, typing_delay):
        """Submit the word with human-like typing"""
        try:
            # Find input field with a more reliable selector
            input_field = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@name='input'][@placeholder='']")
            ))
            input_field.clear()
            
            # More humanlike typing pattern with slight randomness
            for i, char in enumerate(word):
                # Slightly vary typing speed within a word
                current_delay = typing_delay * (0.9 + random.random() * 0.2)
                # Slow down slightly at beginning and end of words
                if i < 2 or i > len(word) - 3:
                    current_delay *= 1.2
                
                input_field.send_keys(char)
                time.sleep(current_delay)

                if random.random() < 0.2:
                    # Type a wrong character and delete it
                    wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                    input_field.send_keys(wrong_char)
                    time.sleep(current_delay / 2)
                    input_field.send_keys(Keys.BACK_SPACE)
                    time.sleep(current_delay / 2)
            
            # Random delay before clicking submit (as humans do)
            time.sleep(random.uniform(0.1, 0.3))
            
            # Click submit using a better selector
            submit_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Enter']")
            ))
            self.driver.execute_script("arguments[0].click();", submit_button)
            
        except Exception as e:
            print(f"Error submitting word: {e}")
            raise e

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
        """More human-like inventory management"""
        try:
            items = self.driver.find_elements(By.CLASS_NAME, "name")
            if not items:
                return

            # Don't always take all items
            num_items = random.randint(1, len(items))
            selected_items = random.sample(items, num_items)

            for item in selected_items:
                # Sometimes hover before clicking
                if random.random() < 0.3:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(item)
                    actions.pause(random.uniform(0.2, 0.8))
                    actions.perform()

                self.simulate_human_mouse_movement(item)
                actions.double_click(item).perform()
                self.random_delay(0.3, 1.2)

        except Exception as e:
            print(f"Error in take_item: {e}")
    
    def grab_agent_loot(self):
        """Grab both loots from agents"""
        try:
            inventory_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Agents']")))
            self.driver.execute_script("arguments[0].click();", inventory_button)
            time.sleep(0.1)

            # list Grab loot buttons //button[text()='Grab Loot']
            grab_loot_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Grab Loot']")
            for button in grab_loot_buttons:
                self.driver.execute_script("arguments[0].click();", button)
                time.sleep(0.1)

        except Exception as e:
            print(f"Error selecting target: {e}")
            raise e
    
    def up_agents(self):   
        """Upgrade agents"""
        try:
            agents_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Agents']")))
            self.driver.execute_script("arguments[0].click();", agents_button)
            time.sleep(0.1)

            # list Upgrade buttons //button[text()='Upgrade']
            upgrade_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Upgrade']")
            for button in upgrade_buttons:
                self.driver.execute_script("arguments[0].click();", button)
                time.sleep(0.1)

        except Exception as e:
            print(f"Error selecting target: {e}")
            raise

    def close_window(self):
        """Close the hacking window with improved error handling"""
        try:
            time.sleep(0.1)  # Increased wait time

            # Try to find and click 'Ok, cool' button first
            try:
                ok_cool_button = self.driver.find_element(By.XPATH, "//button[text()='Ok, cool']")
                self.driver.execute_script("arguments[0].click();", ok_cool_button)
                time.sleep(0.1)
            except:
                pass

            # Find and close all windows
            close_buttons = self.driver.find_elements(By.CLASS_NAME, 'window-close')
            for button in close_buttons:
                try:
                    self.driver.execute_script("arguments[0].click();", button)
                    time.sleep(0.1)
                except:
                    continue

        except Exception as e:
            print(f"Error closing window: {e}")
    
    def check_mail_window(self):
        """Check if mail window is open"""
        try:
            # Look for a window with mail icon and title
            mail_windows = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'window')]//img[contains(@src, 'mail.svg')]/ancestor::div[contains(@class, 'window')]")
            return len(mail_windows) > 0
        except:
            return False

    def hack_loop(self, is_npc):
        """Main hacking loop with improved error handling and retry mechanisms"""
        self.fails = 0
        success_count = 0
        retry_count = 0
        max_retries = 3
        break_time = 1.0 if is_npc else 1.3  # NPC can have slightly faster break time
        
        # Track start time to prevent excessive looping
        start_time = time.time()
        max_duration = 180  # Max 3 minutes in hack loop
        
        while True:
            # Exit if we've been in the loop too long
            if time.time() - start_time > max_duration:
                print("Hack loop time limit exceeded, exiting")
                self.close_window()
                return
                
            try:
                # Handle various dialog boxes that might appear
                self.handle_popups()
                
                # Get current tries
                try:
                    old_tries = self.get_current_tries()
                    print(f"Current tries: {old_tries}")
                    if old_tries <= 0:
                        print("No more tries left, exiting hack loop")
                        self.close_window()
                        return
                except Exception as e:
                    print(f"Could not get current tries: {e}")
                    if retry_count < max_retries:
                        retry_count += 1
                        print(f"Retrying... ({retry_count}/{max_retries})")
                        time.sleep(0.5)
                        continue
                    else:
                        print("Max retries reached, exiting hack loop")
                        self.close_window()
                        return
                
                # Process word and submit
                try:
                    img_src, word, OCR_result = self.process_word()
                    
                    # If we couldn't get a word, retry
                    if not img_src or not word:
                        if retry_count < max_retries:
                            retry_count += 1
                            print(f"Failed to get word, retrying... ({retry_count}/{max_retries})")
                            time.sleep(0.5)
                            continue
                        else:
                            print("Max retries reached, exiting hack loop")
                            self.close_window()
                            return
                    
                    # Reset retry counter after successful word processing
                    retry_count = 0
                    
                    # Randomize typing speed slightly based on word length
                    typing_delay = random.uniform(
                        0.12 if is_npc else 0.18,  # Min delay
                        0.15 if is_npc else 0.22   # Max delay
                    )
                    
                    # Type the word with human-like timing
                    self.submit_word(word, typing_delay)
                    
                    # Wait after submitting
                    adaptive_break = break_time * (0.9 + random.random() * 0.2)  # ±10% randomness
                    time.sleep(adaptive_break)
                    
                    # Verify result
                    try:
                        new_tries = self.get_current_tries()
                        
                        if old_tries > new_tries:
                            print(f"##### FAILED WORD: '{word}' #####")
                            with open('failed-words.txt', 'a') as f:
                                f.write(f"{OCR_result} -- {word}\n")
                            self.fails += 1
                        else:
                            print(f"##### SUCCESS WORD: '{word}' #####")
                            self.save_word_pair_OCR(OCR_result, word)
                            success_count += 1
                            # Reduce break time slightly after consecutive successes for efficiency
                            if success_count > 2 and break_time > 0.8:
                                break_time -= 0.1
                    except Exception as e:
                        print(f"Error checking tries after submission: {e}")
                        # If we can't verify, assume success to keep going
                        pass
                    
                except Exception as e:
                    print(f"Error in word processing/submission: {e}")
                    if retry_count < max_retries:
                        retry_count += 1
                        print(f"Retrying... ({retry_count}/{max_retries})")
                        time.sleep(0.5)
                        continue
                    else:
                        print("Max retries reached, exiting hack loop")
                        self.close_window()
                        return
                
                # Check end conditions
                if self.fails >= 3:
                    print("##### THE END (LOST) - Max fails reached #####")
                    self.close_window()
                    return
                
                try:
                    if self.check_progress():
                        print(f"##### THE END (WON) after {success_count} successful words #####")
                        self.close_window()
                        return
                except Exception as e:
                    print(f"Error checking progress: {e}")
                    # If we can't check progress, continue hacking
                    pass
                
            except Exception as e:
                print(f"Unexpected error in hack loop: {e}")
                if retry_count < max_retries:
                    retry_count += 1
                    print(f"Retrying... ({retry_count}/{max_retries})")
                    time.sleep(0.5)
                    continue
                else:
                    print("Max retries reached, exiting hack loop")
                    self.close_window()
                    return
                    
    def handle_popups(self):
        """Handle various popups and dialogs that might appear"""
        try:
            # Try to handle 'Ok, cool' button
            ok_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Ok') or contains(text(), 'OK') or contains(text(), 'Cool')]")
            for button in ok_buttons:
                if button.is_displayed():
                    self.driver.execute_script("arguments[0].click();", button)
                    time.sleep(0.1)
                    print("Clicked an OK button")
            
            # Check for error messages
            error_messages = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'error') or contains(@class, 'alert')]")
            for message in error_messages:
                if message.is_displayed():
                    print(f"Error message found: {message.text}")
                    # Try to find and click any button to dismiss
                    dismiss_buttons = self.driver.find_elements(By.XPATH, "//button")
                    for button in dismiss_buttons:
                        if button.is_displayed():
                            self.driver.execute_script("arguments[0].click();", button)
                            time.sleep(0.1)
                            print("Clicked a button to dismiss error")
            
            # Check for achievement popups
            achievement_popups = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'Achievement') or contains(text(), 'Unlocked')]")
            for popup in achievement_popups:
                if popup.is_displayed():
                    print(f"Achievement popup found: {popup.text}")
                    # Try to close it
                    close_buttons = self.driver.find_elements(By.XPATH, "//img[contains(@src, 'close.svg')]/ancestor::button")
                    for button in close_buttons:
                        if button.is_displayed():
                            self.driver.execute_script("arguments[0].click();", button)
                            time.sleep(0.1)
                            print("Closed achievement popup")
                            
        except Exception as e:
            print(f"Error handling popups: {e}")
            # Don't raise - this is just a helper function
            
    def auto_bot(self):
        """Auto-bot method with anti-ban measures"""
        while self.run_auto_bot:

            # Random number of hacks per session
            num_hacks = random.randint(3, 5)
            
            for _ in range(num_hacks):
                if self.check_mail_window():
                    print("Mail window detected - stopping auto bot...")
                    self.run_auto_bot = False
                    return
            
                is_npc = self.select_target()
                
                if self.start_hack():
                    self.hack_loop(is_npc)
                    print("Hack complete")
                    self.random_delay(0.5, 2)  # Reduced delay after hack

                    # Take rewards and items
                    self.take_all()
                    self.random_delay(0.1, 0.2)
                else:
                    print("Skipping to next target...")
                    self.close_window()

                
            # Take rewards and items
            self.take_all()
            self.random_delay(0.1, 0.2) 

            self.grab_agent_loot()
            self.random_delay(0.1, 0.2)
            
            self.close_window()
            self.random_delay(0.1, 0.2)

            if self.auto_up:
                self.up_agents()
                self.random_delay(0.1, 0.2)

                self.close_window()
                self.random_delay(0.1, 0.2)
            
            # Add random breaks between sessions
            if is_npc :
                break_time = random.uniform(4, 6)
            else :
                break_time = random.uniform(15, 18)  # Reduced break time
            print(f"Taking a break for {break_time:.1f} seconds...")
            sleep(break_time)

            if random.random() < 0.01:
                self.refresh_and_relogin()


    def run_interactive(self):
        """Interactive main method with anti-ban measures"""
        self.setup_driver()
        self.login()
        try:
            while True:
                command = input("\nCommands:\n"
                              "t - Take all rewards\n"
                              "h - Start hack and loop\n"
                              "c - Close window\n"
                              "s - Select target\n"
                              "r - Refresh and relogin\n"
                              "g - Click green button\n"
                              "l - Grab agent loots\n"
                              "a - Activate auto-bot\n"
                              "q - Quit\n"
                              "Enter command: ").lower()

                if command == 'h':
                    number_of_hacks = input("How many hacks to do? ")
                    for _ in range(int(number_of_hacks)):
                        if self.driver:
                            is_npc = self.select_target()
                            if self.start_hack():  # Only continue if hack started successfully
                                self.hack_loop(is_npc)
                                print("Hack complete")
                            else:
                                print("Skipping to next target...")
                                self.close_window()  # Close the target window
                        else:
                            print("Please setup first (s)")

                elif command == 's':
                    if self.driver:
                        is_npc = self.select_target()
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

                elif command == 't':
                    if self.driver:
                        self.take_all()
                        print("All rewards taken")
                    else:
                        print("Please setup first (s)")
                
                elif command == 'r':
                    if self.driver:
                        self.refresh_and_relogin()
                    else:
                        print("Please setup first (s)")

                elif command =='g':
                    if self.driver:
                        self.click_green_button()
                    else:
                        print("Please setup first (s)")

                elif command == 'l':
                    if self.driver:
                        self.grab_agent_loot()
                    else:
                        print("Please setup first (s)")

                elif command == 'a':
                    print("Auto-bot activated with anti-ban measures")
                    self.run_auto_bot = True
                    self.auto_bot()

                else:
                    print("Invalid command")

        except Exception as e:
            print(f"An error occurred: {e}")
            if self.driver:
                self.driver.quit()
                print("Browser closed due to error")

    def simulate_human_mouse_movement(self, target_element):
        """Simulate human-like mouse movement to a target element"""
        try:
            # Get element position and size
            element_loc = target_element.location
            size = target_element.size
            
            # Calculate target center
            target_x = element_loc['x'] + size['width'] / 2
            target_y = element_loc['y'] + size['height'] / 2
            
            # Get viewport size
            viewport_width = self.driver.execute_script("return window.innerWidth;") or 1024
            viewport_height = self.driver.execute_script("return window.innerHeight;") or 768
            
            # Start from a random position within viewport
            start_x = random.randint(0, viewport_width)
            start_y = random.randint(0, viewport_height)
            
            # Create action chain
            actions = ActionChains(self.driver)
            
            # Generate curve points
            points = []
            steps = random.randint(3, 5)  # Reduced number of steps
            
            # Calculate movement needed
            delta_x = target_x - start_x
            delta_y = target_y - start_y
            
            for i in range(steps):
                progress = i / steps
                
                # Add curve using sine wave with smaller offsets
                curve_x = delta_x * progress + math.sin(progress * math.pi) * random.randint(5, 15)
                curve_y = delta_y * progress + math.sin(progress * math.pi) * random.randint(5, 15)
                
                points.append((curve_x / steps, curve_y / steps))
            
            # Execute movement
            for (x, y) in points:
                actions.move_by_offset(x, y)
                actions.pause(random.uniform(0.01, 0.03))  # Shorter pauses
            
            # Final movement
            actions.move_to_element(target_element)
            actions.pause(0.1)
            actions.perform()
            
        except Exception as e:
            print(f"Error in mouse movement: {e}")
            # Fallback to direct movement
            try:
                ActionChains(self.driver).move_to_element(target_element).click().perform()
            except:
                # Last resort: JavaScript click
                try:
                    self.driver.execute_script("arguments[0].click();", target_element)
                except:
                    pass

if __name__ == "__main__":
    bot = HackerIOBot()
    bot.run_interactive()