# Import booking class
from booking.booking import Booking
import time
from datetime import datetime, timedelta

todaysDate = datetime.now()
weekDate = datetime.now() + timedelta(days=7)
todaysDate = todaysDate.date()
weekDate = weekDate.date()

# without teardown=True browser will remain open
with Booking() as bot:
    bot.land_first_page()
    bot.change_currency("EUR")
    bot.select_location("Paris")
    bot.select_dates(todaysDate, weekDate)
    bot.select_occupants(4)
    bot.click_search()
    bot.apply_filtrations()
    # keep open to see changes made
    time.sleep(10)
    print("Exiting...")
