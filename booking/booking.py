# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import booking.constants as const
from booking.booking_filtration import BookingFiltration
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
        # open webiste
        self.get(const.BASE_URL)
        # try and check for popup
        try:
            # if there is the presence of a popup
            if wait.until(
                EC.presence_of_element_located(
                    # element filtration
                    (By.CLASS_NAME, "e5aa33035e"),
                )
            ):
                # find the close button of popup
                closeBtn = self.find_element(
                    By.CLASS_NAME,
                    "fc63351294.a822bdf511.e3c025e003.fa565176a8.f7db01295e.c334e6f658.ae1678b153",
                )
                # click on popup
                closeBtn.click()
        # if there is no popup continute executing code
        except:
            print("No popup: continuing..")

    # change website currency for universal
    def change_currency(self, currency):
        # grabbing currency element
        currencyElement = self.find_element(
            By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]'
        )
        # click on currenct element
        currencyElement.click()
        # Selecting span by filtering out by span based on currency param
        currencyText = self.find_elements(By.CLASS_NAME, "ea1163d21f")
        # try and see if texts match
        try:
            # loop through currenecy text
            for text in currencyText:
                # if one matches our currency param
                if text.text == currency:
                    # click on that text
                    text.click()
        # if a double element is found after going stale continue program
        except:
            print("Second element located: continuing...")

    # select location
    def select_location(self, location):
        # find search field element
        searchField = self.find_element(By.NAME, "ss")
        # clear it best practice
        searchField.clear()
        # send place
        searchField.send_keys(location)
        # wait for element generation before clicking on first item
        time.sleep(1)
        # grab the first result element
        firstResult = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "a80e7dc237"))
        )
        # click on element
        firstResult.click()

    # select dates
    def select_dates(self, check_in, check_out):
        # find check in element
        checkInEl = wait.until(
            # when present sent check in date value
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f'span[data-date="{check_in}"]')
            )
        )
        # click check in element
        checkInEl.click()
        # find check out element
        checkOutEl = wait.until(
            EC.presence_of_element_located(
                # when present sent check out date value
                (By.CSS_SELECTOR, f'span[data-date="{check_out}"]')
            )
        )
        # click check out element
        checkOutEl.click()

    # select occupants count
    def select_occupants(self, adults):
        # find selection element
        selectionTab = self.find_element(
            By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]'
        )
        # click on selection element
        selectionTab.click()
        # find the adults section
        adultSelection = self.find_element(By.ID, "group_adults")
        # decrease to starting point
        while True:
            # find decrease button
            decreaseBtn = self.find_element(
                By.CLASS_NAME,
                "fc63351294.a822bdf511.e3c025e003.fa565176a8.f7db01295e.c334e6f658.e1b7cfea84.cd7aa7c891",
            )
            # click on decrease button
            decreaseBtn.click()
            countSpan = self.find_element(By.ID, "group_adults")
            # gives elements adult count value
            adultsVal = countSpan.get_attribute("value")
            # if value of adults = 1, then break
            if int(adultsVal) == 1:
                break
        # wait before increasing to avoid hanging
        time.sleep(0.5)
        # find increase button element
        increaseBtn = self.find_element(
            By.CLASS_NAME,
            "fc63351294.a822bdf511.e3c025e003.fa565176a8.f7db01295e.c334e6f658.e1b7cfea84.d64a4ea64d",
        )
        # increase param count minus 1
        for i in range(adults - 1):
            # click
            increaseBtn.click()
        # select done button
        doneBtn = self.find_element(
            By.CLASS_NAME,
            "fc63351294.a822bdf511.e2b4ffd73d.f7db01295e.c938084447.a9a04704ee.d285d0ebe9",
        )
        # click done button
        doneBtn.click()

    # search deals
    def click_search(self):
        # find search button element
        searchBtn = self.find_element(
            By.CLASS_NAME,
            "fc63351294.a822bdf511.d4b6b7a9e7.cfb238afa1.c938084447.f4605622ad.aa11d0d5cd",
        )
        # click search button
        searchBtn.click()

    # make new filtrations class to organize functionally
    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(3, 4, 5)
        filtration.sort_by_lowest()
