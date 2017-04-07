from pyvirtualdisplay import Display
from selenium import webdriver
import sys
from digi_selenium_scraper_daily_functions import (
    download_material_for_day)
from digi_selenium_scraper_common_functions import (
    get_datetime_from_arg)
import getopt
import datetime


def get_start_params(argv):
    start_date = '1911-01-01'
    end_date = '1920-01-01'
    material_type = 'journals'

    try:
        opts, args = getopt.getopt(argv, "",
                                   ["start_date=",
                                    "end_date=",
                                    "material_type="]
                                   )
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == "--start_date":
            start_date = arg
        elif opt == "--end_date":
            end_date = arg
        elif opt == "--material_type":
            material_type = arg
    return(start_date, end_date, material_type)


display = Display(visible=0, size=(800, 600))
display.start()
browser = webdriver.Chrome()
browser.implicitly_wait(30)
browser.set_window_size(800, 600)


start_date, end_date, material_type = get_start_params(sys.argv[1:])
print("Scraping from " + start_date + " to " + end_date)
start_datetime = get_datetime_from_arg(start_date)
end_datetime = get_datetime_from_arg(end_date)
scraping_datetime = start_datetime


while scraping_datetime <= end_datetime:
    print("Scraping date: " + str(scraping_datetime))
    download_material_for_day(year=scraping_datetime.year,
                              month=scraping_datetime.month,
                              day=scraping_datetime.day,
                              material_type=material_type,
                              browser=browser)
    scraping_datetime = scraping_datetime + datetime.timedelta(days=1)


browser.quit()
display.stop()

# usage:
# python digi_selenium_scraper_pagenumbers.py --start_date 1911-01-03 --end_date 1911-12-31 --material_type journals
# python digi_selenium_scraper_pagenumbers.py --start_date 1911-01-03 --end_date 1911-12-31 --material_type newspapers
# python digi_selenium_scraper_pagenumbers.py --start_date 1913-01-01 --end_date 1913-12-31 --material_type newspapers