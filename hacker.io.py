# hacker_io_bot.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from OCR import extract_text_from_base64_image

class HackerIOBot:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.saved_words = self.load_saved_words()
        self.fails = 0

    def setup_driver(self):
        """Initialize and configure the Chrome WebDriver"""
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)
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

    def save_word_pair(self, img_src, extracted_text):
        """Save successful word-image pairs"""
        try:
            self.saved_words[img_src] = extracted_text
            with open("saved-words.json", "w") as file:
                json.dump(self.saved_words, file, indent=4)
        except Exception as e:
            print(f"Error saving word pair: {e}")

    def login(self):
        """Handle the login process"""
        name_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="input"]')))
        name_input.send_keys("Los Valettos")
        
        play_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.grey.svelte-ec9kqa")))
        play_button.click()
        time.sleep(0.2)

    def select_target(self):
        """Select a target to hack"""
        try:
            # Wait for any existing windows to be closeable
            time.sleep(0.2)
            
            # Close any open windows first
            try:
                close_buttons = self.driver.find_elements(By.CLASS_NAME, 'window-close')
                for button in close_buttons:
                    self.driver.execute_script("arguments[0].click();", button)
            except:
                pass
            
            # Wait and click target list
            target_list = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Target List']"))
            )
            self.driver.execute_script("arguments[0].click();", target_list)
            time.sleep(0.2)

            # Wait and click first target
            real_target_list = self.wait.until(
                EC.element_to_be_clickable((By.ID, 'list'))
            )
            first_target = real_target_list.find_element(By.XPATH, "./div[1]")
            self.driver.execute_script("arguments[0].click();", first_target)
            
        except Exception as e:
            print(f"Error selecting target: {e}")
            raise e

    def start_hack(self):
        """Initiate the hacking process"""
        hack_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Hack']")))
        hack_button.click()

        port_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Port ')]")))
        port_button.click()
        time.sleep(0.2)

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
        time.sleep(0.2)

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

    def close_window(self):
        """Close the hacking window"""
        try:
            # Wait for the close button and ensure it's clickable
            close_button = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'window-close'))
            )
            
            # Scroll the button into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
            
            # Add a small delay to let the scroll complete
            time.sleep(0.5)
            
            # Try to click using JavaScript if normal click fails
            try:
                close_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", close_button)
            
        except Exception as e:
            print(f"Error closing window: {e}")
            # Try alternative close method using escape key
            from selenium.webdriver.common.keys import Keys
            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

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

                if self.fails == 3 :
                    print("##### THE END LOST #####")
                    # Closes windows while the is windows to close
                    for _ in range(5):
                        self.close_window()
                    break
                    
                if self.check_progress():
                    print("##### THE END WON #####")
                    # Closes windows while the is windows to close
                    for _ in range(5):
                        self.close_window()
                    break

                time.sleep(0.2)

            except Exception as e:
                print(f"Error in hack loop: {e}")
                break

    def run_interactive(self):
        """Interactive main method"""
        self.setup_driver()
        self.login()
        try:
            while True:
                self.select_target()
                self.start_hack()
                self.hack_loop()
                """
                command = input("\nCommands:\n"
                              "h - Start hack and loop\n"
                              "c - Close window\n"
                              "q - Quit\n"
                              "Enter command: ").lower()

                if command == 'h':
                    if self.driver:
                        self.select_target()
                        self.start_hack()
                        self.hack_loop()
                        print("Hack complete")
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

                else:
                    print("Invalid command")
                """

        except Exception as e:
            print(f"An error occurred: {e}")
            if self.driver:
                self.driver.quit()
                print("Browser closed due to error")

if __name__ == "__main__":
    bot = HackerIOBot()
    bot.run_interactive()
