# Import booking class
from booking.booking import Booking
import time

# without teardown=True browser will remain open
with Booking() as bot:
    bot.land_first_page()
    bot.change_currency("EUR")
    bot.select_location("Paris")
    bot.select_dates("2023-07-16", "2023-08-16")
    bot.select_occupants(4)
    bot.click_search()
    time.sleep(20)
    print("Exiting...")
