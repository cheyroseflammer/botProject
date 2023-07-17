# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import booking.constants as const
import time
import os


# Define booking class
class Booking(webdriver.Chrome):
    # initialize driver
    def __init__(self, driver_path="C:\Selenium\chromedriver.exe", teardown=False):
        self.driver_path = driver_path
        # teardown down
        self.teardown = teardown
        # access local enviroment for driver
        os.environ["PATH"] += self.driver_path
        # initialize super class
        super(Booking, self).__init__()
        # global implicitly wait function
        global wait
        wait = WebDriverWait(self, 10)

    # tear down function that doesnt even work :)
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    # open website
    def land_first_page(self):
        self.get(const.BASE_URL)
        # close popup
        try:
            if wait.until(
                EC.presence_of_element_located(
                    # element filtration
                    (By.CLASS_NAME, "e5aa33035e"),
                )
            ):
                closeBtn = self.find_element(
                    By.CLASS_NAME,
                    "fc63351294.a822bdf511.e3c025e003.fa565176a8.f7db01295e.c334e6f658.ae1678b153",
                )
                closeBtn.click()
                time.sleep(1)
        except:
            print("No popup: continuing..")

    ########### DEBUG STALE ERROR LATER ##############
    # change website currency for universal
    def change_currency(self, currency):
        # grabbing currency element
        currencyElement = self.find_element(
            By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]'
        )
        currencyElement.click()
        # Selecting span by filtering out by span based on currency param
        currencyText = self.find_elements(By.CLASS_NAME, "ea1163d21f")
        try:
            for text in currencyText:
                if text.text == currency:
                    text.click()
        except:
            print("Second element located: continuing...")

    # select location
    def select_location(self, location):
        search_field = self.find_element(By.NAME, "ss")
        # clear it best practice
        search_field.clear()
        # send place
        search_field.send_keys(location)
        # wait before clicking on first item
        time.sleep(1)
        first_result = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "a80e7dc237"))
        )
        first_result.click()

    ####### have to automate range selection for months in advance ########
    # select dates
    def select_dates(self, check_in, check_out):
        checkInEl = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f'span[data-date="{check_in}"]')
            )
        )
        checkInEl.click()
        checkOutEl = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f'span[data-date="{check_out}"]')
            )
        )
        checkOutEl.click()

    # select occupants count
    def select_occupants(self, adults):
        selectionTab = self.find_element(
            By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]'
        )
        selectionTab.click()
        adultSelection = self.find_element(By.ID, "group_adults")
        # decrease to starting point

        while True:
            decreaseBtn = self.find_element(
                By.CLASS_NAME,
                "fc63351294.a822bdf511.e3c025e003.fa565176a8.f7db01295e.c334e6f658.e1b7cfea84.cd7aa7c891",
            )
            decreaseBtn.click()
            # if value of adults = 1, then break
            countSpan = self.find_element(By.ID, "group_adults")
            # gives back adult count
            adultsVal = countSpan.get_attribute("value")
            if int(adultsVal) == 1:
                break
        time.sleep(0.5)
        increaseBtn = self.find_element(
            By.XPATH,
            "/html/body/div[2]/div[2]/div/div/form/div[1]/div[3]/div/div/div/div/div[1]/div[2]/button[2]",
        )
        for i in range(adults - 1):
            increaseBtn.click()
        # CHILD (NEEDS MORE  INFO COMMENT OUT)
        increaseBtnTwo = self.find_element(
            By.XPATH,
            "/html/body/div[2]/div[2]/div/div/form/div[1]/div[3]/div/div/div/div/div[2]/div[2]/button[2]",
        )
        # CHILD AGE
        # childSelection = self.find_element(By.ID, "group_children")
        # for i in range(children):
        #     increaseBtnTwo.click()

    def click_search(self):
        print("Hello")
