from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

# Page Object Model Class for IMDb Search Page
class IMDbSearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)  # Increased wait time

    # Locators
    SEARCH_BOX = (By.ID, 'name')
    GENDER_DROPDOWN = (By.ID, 'gender')
    GENDER_OPTION_MALE = (By.XPATH, "//option[@value='male']")
    STARMETER_MIN = (By.NAME, 'starMeter-min')
    STARMETER_MAX = (By.NAME, 'starMeter-max')
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Actions with Exception Handling
    def enter_name(self, name):
        try:
            search_box = self.wait.until(EC.presence_of_element_located(self.SEARCH_BOX))
            search_box.clear()
            search_box.send_keys(name)
        except TimeoutException:
            print("Search box not found")

    def select_gender(self):
        try:
            gender_dropdown = self.wait.until(EC.element_to_be_clickable(self.GENDER_DROPDOWN))
            gender_dropdown.click()
            male_option = self.wait.until(EC.element_to_be_clickable(self.GENDER_OPTION_MALE))
            male_option.click()
        except TimeoutException:
            print("Gender dropdown or option not found")

    def set_starmeter_range(self, min_value, max_value):
        try:
            starmeter_min = self.wait.until(EC.presence_of_element_located(self.STARMETER_MIN))
            starmeter_min.clear()
            starmeter_min.send_keys(min_value)

            starmeter_max = self.wait.until(EC.presence_of_element_located(self.STARMETER_MAX))
            starmeter_max.clear()
            starmeter_max.send_keys(max_value)
        except TimeoutException:
            print("Starmeter range inputs not found")

    def click_search(self):
        try:
            search_button = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
            search_button.click()
        except TimeoutException:
            print("Search button not clickable")

# Main Execution Function
def main():
    # Setup Chrome WebDriver with error handling for driver issues
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
    except Exception as e:
        print(f"Webdriver setup failed: {e}")
        return

    # Go to IMDb search name page
    try:
        driver.get('https://www.imdb.com/search/name/')
    except Exception as e:
        print(f"Failed to load IMDb page: {e}")
        driver.quit()
        return

    # Create an instance of the IMDbSearchPage
    search_page = IMDbSearchPage(driver)

    # Perform actions on the page
    search_page.enter_name("Leonardo DiCaprio")
    search_page.select_gender()
    search_page.set_starmeter_range("1", "100")
    search_page.click_search()

    # Verify the search result
    try:
        if "Leonardo DiCaprio" in driver.page_source:
            print("Search successful: Leonardo DiCaprio found!")
        else:
            print("Search failed: Leonardo DiCaprio not found.")
    except Exception as e:
        print(f"An error occurred during search result validation: {e}")

    # Close the browser
    driver.quit()

# Run the script
if __name__ == "__main__":
    main()