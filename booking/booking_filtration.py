# This file includes a class with instance methods to apply filtrations.
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time


class BookingFiltration:
    # driver:WebDriver sets type to we have access to selenium methods
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # apply star filtrations
    def apply_star_rating(self, *star_values):
        # grab filtration box
        star_filtration_box = self.driver.find_element(
            By.ID, "filter_group_class_:R14q:"
        )
        # grab all child elements of the filtration box
        star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, "*")
        # loop through parameter
        for star_value in star_values:
            # loop through child elements
            for star_element in star_child_elements:
                # if our parameters match the innerHTML
                if (
                    str(star_element.get_attribute("innerHTML")).strip()
                    == f"{star_value} stars"
                ):
                    # click that element
                    star_element.click()

    # sort by lowest price
    def sort_by_lowest(self):
        # find sort dropdown element
        sort_by_dropdown = self.driver.find_element(
            By.CSS_SELECTOR,
            "button[data-testid='sorters-dropdown-trigger']",
        )
        # click on dropdown
        sort_by_dropdown.click()
        # find sort by lowest price element
        lowest_price = self.driver.find_element(
            By.CSS_SELECTOR,
            "button[data-id='price']",
        )
        # click on lowest price
        lowest_price.click()
