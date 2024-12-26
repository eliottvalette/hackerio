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
from selenium.webdriver.common.keys import Keys

load_dotenv()
username = 'ESpeculos3749'
email = 'heteho5137@pixdd.com'

password = os.getenv("PASSWORD")
class HackerIOBot:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.saved_words_OCR = self.load_saved_words_OCR()
        self.fails = 0
        self.use_proxy = False
        # List of Chrome user agents from different versions and platforms
        self.chrome_agents = [
            # Windows Chrome
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # Mac Chrome
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            # Linux Chrome
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        ]

        self.width = 0
        self.height = 0

    def setup_driver(self):
        """Initialize and configure the Chrome WebDriver"""
        chrome_options = webdriver.ChromeOptions()
        
        # Essential stealth settings
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Add more realistic browser settings
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument(f'--window-size={random.randint(1024, 1920)},{random.randint(768, 1080)}')
        chrome_options.add_argument('--start-maximized')
        
        # Add random user agent
        user_agent = random.choice(self.chrome_agents)
        chrome_options.add_argument(f'user-agent={user_agent}')
        
        # Add connection settings
        chrome_options.add_argument('--disable-application-cache')
        chrome_options.add_argument('--disable-network-throttling')
        chrome_options.add_argument('--dns-prefetch-disable')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 5)  # Increased timeout
            
            # Set window size
            self.width = self.driver.execute_script("return window.innerWidth;")
            self.height = self.driver.execute_script("return window.innerHeight;")
            
            # Add stealth script
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            # Try to connect with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    self.driver.get("https://s0urce.io/")
                    # Wait for page to load
                    self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    break
                except Exception as e:
                    print(f"Connection attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(random.uniform(2, 5))
                        continue
                    else:
                        raise e
                    
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

    def login(self, unknown=True):
        """Handle the login process"""
        try:
            # Initial delay to ensure page is fully loaded
    time.sleep(2)

            if unknown:
                # Wait for input field with better error handling
                try:
                    name_input = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="input"]'))
                    )
                    
                    # Verify element is actually visible and interactable
                    if not name_input.is_displayed() or not name_input.is_enabled():
                        raise Exception("Input field is not visible or enabled")
                    
                    # Generate username
                    username_length = random.randint(6, 12)
                    username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=username_length))
                    
                    # Type username with natural delays
                    for char in username:
                        name_input.send_keys(char)
                        time.sleep(random.uniform(0.05, 0.15))
                    
                    # Wait for play button
                    play_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.grey.svelte-ec9kqa"))
                    )
                    
                    # Click play button
                    play_button.click()
                    time.sleep(1)  # Wait for login to complete
                    
                except Exception as e:
                    print(f"Error finding or interacting with login elements: {e}")
                    raise e
                
        except Exception as e:
            print(f"Error during login: {e}")
            raise e

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

    def random_delay(self, min_delay=0.05, max_delay=0.15):
        """Add random delay between actions"""
        if random.random() < 0.1:  # 10% chance of longer delay
            sleep(random.uniform(0.2, 0.5))
        else:
            sleep(random.uniform(min_delay, max_delay))

    def submit_word(self, word):
        """Submit the word with human-like typing"""
        try:
            input_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="input"]')))
            
            # Sometimes make typing mistakes
            if random.random() < 0.1:  # 10% chance of typo
                typo_index = random.randint(0, len(word)-1)
                word = word[:typo_index] + random.choice('abcdefghijklmnopqrstuvwxyz') + word[typo_index:]
            
            # Type with variable speed
            for i, char in enumerate(word):
                # Simulate natural typing rhythm
                if i > 0:
                    # Longer pauses for certain key combinations
                    prev_char = word[i-1]
                    if prev_char.isupper() or char.isupper():
                        time.sleep(random.uniform(0.1, 0.3))
                    elif prev_char in 'aeiou' and char in 'aeiou':
                        time.sleep(random.uniform(0.08, 0.15))
                    else:
                        time.sleep(random.uniform(0.05, 0.1))
                
                input_field.send_keys(char)
            
            # Sometimes backspace and correct
            if random.random() < 0.05:  # 5% chance
                input_field.send_keys(Keys.BACKSPACE)
                time.sleep(random.uniform(0.1, 0.3))
                input_field.send_keys(word[-1])
            
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
                    actions.pause(random.uniform(0.1, 0.4))
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
        """Main hacking loop with human-like errors"""
        self.fails = 0
        consecutive_successes = 0
        
        while True:
            try:
                # Sometimes get distracted
                if random.random() < 0.05:  # 5% chance
                    time.sleep(random.uniform(2, 5))
                
                # Sometimes click wrong things
                if random.random() < 0.03:  # 3% chance
                    random_element = self.driver.find_element(By.TAG_NAME, "div")
                    self.simulate_human_mouse_movement(random_element)
                    time.sleep(random.uniform(0.2, 0.5))
                
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

                # Add variable success patterns
                if consecutive_successes > random.randint(3, 6):
                    time.sleep(random.uniform(1, 3))
                    consecutive_successes = 0
                    
            except Exception as e:
                print(f"Error in hack loop: {e}")
                time.sleep(random.uniform(1, 3))
                self.fails += 1

    def run_interactive(self):
        """Interactive main method"""
        session_count = 0
        
        while True:
            try:
                self.setup_driver()
                self.login()
                
                # Random number of hacks before break
                max_hacks = random.randint(15, 25)
                hacks_done = 0
                
                while hacks_done < max_hacks:
                    # Your existing hack loop code...
                    hacks_done += 1
                
                # Take a longer break between sessions
                session_count += 1
                if session_count % 3 == 0:  # Every 3 sessions
                    break_time = random.uniform(300, 600)  # 5-10 minutes
                    print(f"Taking a longer break: {break_time/60:.1f} minutes")
                    time.sleep(break_time)
                
                # Close and restart browser
                self.driver.quit()
                time.sleep(random.uniform(10, 30))
                
            except Exception as e:
                print(f"Session error: {e}")
                if self.driver:
                    self.driver.quit()
                time.sleep(random.uniform(60, 120))

    def simulate_human_mouse_movement(self, target_element):
        """Simulate human-like mouse movement to a target element"""
        try:
            actions = ActionChains(self.driver)
            
            # Get element position and size
            element_loc = target_element.location
            size = target_element.size
            
            # Calculate target center
            target_x = element_loc['x'] + size['width'] / 2
            target_y = element_loc['y'] + size['height'] / 2
            
            # Get viewport size (reduced to 1/4 for faster movements)
            viewport_width = self.width / 4
            viewport_height = self.height / 4
            
            # More varied starting positions
            start_x = random.randint(viewport_width / 2, viewport_height / 2)
            start_y = random.randint(viewport_width / 2, viewport_height / 2)
            
            # Vary movement patterns
            pattern = random.choice(['direct', 'curved', 'zigzag'])
            steps = random.randint(3, 8)  # More variation
            
            for i in range(steps):
                progress = i / steps
                if pattern == 'direct':
                    offset = random.randint(1, 5)
                elif pattern == 'curved':
                    offset = math.sin(progress * math.pi) * random.randint(10, 30)
                else:  # zigzag
                    offset = ((-1) ** i) * random.randint(10, 20)
                    
                actions.move_by_offset(start_x + offset, start_y + offset)
                # More human-like delay variation
                actions.pause(random.uniform(0.001, 0.03))
            
            # Final movement
            actions.move_to_element(target_element)
            actions.pause(0.01)  # Reduced from 0.1-0.2
            actions.perform()
            
        except Exception as e:
            print(f"Error in mouse movement: {e}")
            # Quick fallback
            try:
                ActionChains(self.driver).move_to_element(target_element).perform()
            except:
                pass

if __name__ == "__main__":
    bot = HackerIOBot()
    bot.run_interactive()
