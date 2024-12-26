# hacker_io.py

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
from time import sleep
import math

load_dotenv()
username = 'PlayerSafe71889'
email = 'pefot88659@pixdd.com'

password = os.getenv("PASSWORD")
class HackerIOBot:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.saved_words_OCR = self.load_saved_words_OCR()
        self.fails = 0

    def setup_driver(self):
        """Initialize and configure the Chrome WebDriver"""
        # Create Chrome options
        chrome_options = webdriver.ChromeOptions()
        # Disable cache, cookies, and other storage
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-cache")
        chrome_options.add_argument("--disable-application-cache")
        chrome_options.add_argument("--disable-offline-load-stale-cache")
        chrome_options.add_argument("--disk-cache-size=0")
        chrome_options.add_argument("--disable-gpu-shader-disk-cache")
        chrome_options.add_argument("--media-cache-size=0")
        chrome_options.add_argument("--disable-extensions")
        # Disable location services
        chrome_options.add_argument("--disable-geolocation")
        # Disable various features that could track state
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-web-security")
        
        # Initialize the driver with our options
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 2)
        self.driver.maximize_window()
        self.driver.get("https://s0urce.io/")

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
        if unknown:
            name_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="input"]')))
            # Random name with 7 letters
            name_input.send_keys("".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=7)))
            
            play_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.grey.svelte-ec9kqa")))
            play_button.click()
        else :
            login_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "green")))
            login_button.click()

            auth_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/auth/twitter']")) )
            auth_link.click()

            time.sleep(3)

            username_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="text"]')))
            username_input.send_keys(username)

            next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]")))
            next_button.click()

            time.sleep(3)

            try :
                email_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="text"]')))
                email_input.send_keys(email)

                next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]")))
                next_button.click()
            except :
                pass

            time.sleep(3)

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
        """Select a target to hack with mouse movement"""
        try:
            time.sleep(0.1)
            
            # Move to and click target list
            target_list = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Target List']")))
            self.simulate_human_mouse_movement(target_list)
            target_list.click()
            time.sleep(0.1)

            # Move to and click random target
            real_target_list = self.wait.until(EC.element_to_be_clickable((By.ID, 'list')))
            targets = real_target_list.find_elements(By.XPATH, "./div")
            random_target = random.choice(targets[:2] + targets[5:])
            self.simulate_human_mouse_movement(random_target)
            random_target.click()
            
        except Exception as e:
            print(f"Error selecting target: {e}")
            return

    def start_hack(self):
        """Initiate the hacking process with mouse movement"""
        try:
            time.sleep(0.1)
            hack_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Hack']")))
            
            if 'cantClick' in hack_button.get_attribute("class"):
                print("Hack button is not clickable (timer active). Skipping...")
                return False
            
            # Move to and click hack button
            self.simulate_human_mouse_movement(hack_button)
            hack_button.click()
            
            # Move to and click port button
            port_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Port ')]")))
            self.simulate_human_mouse_movement(port_button)
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
        
        text, OCR_result = extract_text_from_base64_image(img_src)
        print(f"Extracted text: {text}")
        return img_src, text, OCR_result

    def random_delay(self, min_delay=0.1, max_delay=0.3):
        """Add random delay between actions"""
        sleep(random.uniform(min_delay, max_delay))

    def submit_word(self, word):
        """Submit the word with human-like typing and mouse movement"""
        try:
            input_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="input"]')))
            
            # Move mouse to input field naturally
            self.simulate_human_mouse_movement(input_field)
            input_field.click()
            
            # Type with variable speed
            for char in word:
                input_field.send_keys(char)
                self.random_delay(0.05, 0.3)
            
            # Move to and click submit button
            submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Enter']")))
            self.simulate_human_mouse_movement(submit_button)
            submit_button.click()
            
        except Exception as e:
            print(f"Error submitting word: {e}")

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

                sleep(0.1)
                new_tries = self.get_current_tries()

                if old_tries > new_tries:
                    print("##### FAILED #####")
                    with open('failed-words.txt', 'a') as f:
                        f.write(f"{OCR_result} -- {word}\n")
                    self.fails += 1
                else:
                    print("##### SUCCESS #####")
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
        """Interactive main method with anti-ban measures"""
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
                    print("Auto-bot activated with anti-ban measures")
                    while True:
                        # Random number of hacks per session
                        num_hacks = random.randint(5, 8)
                        
                        for _ in range(num_hacks):
                            self.select_target()
                            self.random_delay(0.075, 0.175)  # Random delay between targets (was 0.3, 0.7)
                            
                            if self.start_hack():
                                self.hack_loop()
                                print("Hack complete")
                                self.random_delay(0.125, 0.25)  # Random delay after hack (was 0.5, 1.0)
                            else:
                                print("Skipping to next target...")
                                self.close_window()
                            
                        # Take rewards and items
                        self.take_all()
                        self.random_delay(0.25, 0.5)  # Longer delay after taking rewards (was 1.0, 2.0)
                        
                        self.open_inventory()
                        self.random_delay(0.125, 0.25)  # (was 0.5, 1.0)
                        
                        self.take_item()
                        self.random_delay(0.125, 0.25)  # (was 0.5, 1.0)
                        
                        self.close_window()
                        self.random_delay(0.075, 0.175)  # (was 0.3, 0.7)
                        
                        # Add random breaks between sessions
                        if random.random() < 0.2:  # 20% chance of taking a break
                            break_time = random.uniform(7.5, 15)  # (was 30, 60)
                            print(f"Taking a break for {break_time:.1f} seconds...")
                            sleep(break_time)

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
            # Create action chain
            actions = ActionChains(self.driver)
            
            # First move to element (to get current position)
            actions.move_to_element(target_element)
            actions.perform()
            
            # Get current mouse position
            current_mouse = self.driver.execute_script(
                "return {x: arguments[0].screenX, y: arguments[0].screenY}",
                target_element
            )
            
            # Get element position
            element_loc = target_element.location
            
            # Calculate relative movement needed
            delta_x = element_loc['x'] - current_mouse['x']
            delta_y = element_loc['y'] - current_mouse['y']
            
            # Create new action chain for curved movement
            actions = ActionChains(self.driver)
            
            # Generate curve points
            points = []
            steps = random.randint(5, 10)
            for i in range(steps):
                progress = i / steps
                
                # Add curve using sine wave
                curve_x = delta_x * progress + math.sin(progress * math.pi) * random.randint(10, 30)
                curve_y = delta_y * progress + math.sin(progress * math.pi) * random.randint(10, 30)
                
                points.append((curve_x, curve_y))
            
            # Execute curved movement
            for (x, y) in points:
                actions.move_by_offset(x, y)
                actions.pause(random.uniform(0.01, 0.05))
            
            # Final precise movement to element
            actions.move_to_element(target_element)
            actions.pause(random.uniform(0.1, 0.2))
            actions.perform()
            
        except Exception as e:
            print(f"Error in mouse movement: {e}")
            # Fallback to direct movement if curved movement fails
            try:
                ActionChains(self.driver).move_to_element(target_element).perform()
            except:
                pass

if __name__ == "__main__":
    bot = HackerIOBot()
    bot.run_interactive()
