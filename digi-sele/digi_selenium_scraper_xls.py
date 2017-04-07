# http://thiagomarzagao.com/2013/11/14/webscraping-with-selenium-part-2/

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import random
import time
import datetime
from pyvirtualdisplay import Display
import glob
from digi_selenium_scraper_common_functions import (
    convert_day_or_month_to_str,
    # convert_day_or_month_range_to_str,
    get_datetime_from_arg,
    csv_from_excel,
    get_daylist_for_month)
import getopt
import sys


# def fetch_newspaper_csv_for_day(year, month, day,
#                                 output_dir='output/test/'):

#     url_start = ('http://digi.kansalliskirjasto.fi/sanomalehti/search' +
#                  '?query=&requireAllKeywords=true' +
#                  '&fuzzy=false&hasIllustrations=false&startDate=')
#     url_mid = '&endDate='
#     url_end = '&orderBy=DATE&pages=&resultMode=TEXT&page=1'
#     url_date = '-'.join([str(year), str(month), str(day)])
#     url_to_process = url_start + url_date + url_mid + url_date + url_end

#     savedir = (output_dir +
#                ('/'.join([str(year), str(month), str(day)])))
#     if not os.path.exists(savedir):
#         os.makedirs(savedir)

#     downdir = os.path.join(os.getcwd(), savedir)

#     prefs = {'download.default_directory': downdir}
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_experimental_option('prefs', prefs)
#     browser = webdriver.Chrome(chrome_options=chrome_options)
#     browser.implicitly_wait(60)
#     browser.set_window_size(800, 600)

#     browser.get(url_to_process)
#     try:
#         download_button = browser.find_element_by_xpath(
#             '//*[@ng-if="ctrl.excelDownloadUrl"]')
#         download_button.click()
#         while not glob.glob(downdir + "/*.xlsx"):
#             time.sleep(1)
#             print("waiting 1 sec for download to finish...")

#         # orig_file = downdir + "/" + os.listdir(downdir)[0]
#         orig_file = downdir + "/" + ("serial-publications--" +
#                                      str(year) + str(month) + str(day) + '-' +
#                                      str(year) + str(month) + str(day) +
#                                      ".xlsx")
#         # new_filename = downdir + "/" + 'newspapers-' + url_date + ".xlsx"
#         # os.rename(orig_file, new_filename)

#         new_csv_filename = downdir + "/" + 'newspapers-' + url_date + ".csv"
#         csv_from_excel(orig_file,
#                        new_csv_filename)

#     except NoSuchElementException:
#         empty_date_filename = downdir + "/" + "empty.txt"
#         with open(empty_date_filename, 'w') as emptyfile:
#             emptyfile.write("no hits for this date!")

#     browser.quit()


def fetch_csv_for_day(year, month, day, browser,
                      material_type='journals',
                      temp_down_dir='download_temp/',
                      output_dir='output/test/'):

    month = convert_day_or_month_to_str(month)
    day = convert_day_or_month_to_str(day)

    if material_type == 'journals':
        material_url = 'aikakausi'
    else:
        material_url = 'sanomalehti'

    url_start = ('http://digi.kansalliskirjasto.fi/' + material_url +
                 '/search?query=&requireAllKeywords=true' +
                 '&fuzzy=false&hasIllustrations=false&startDate=')
    url_mid = '&endDate='
    url_end = '&orderBy=DATE&pages=&resultMode=TEXT&page=1'
    url_date = '-'.join([str(year), str(month), str(day)])
    url_to_process = url_start + url_date + url_mid + url_date + url_end

    savedir = (output_dir +
               ('/'.join([str(year), str(month), str(day)])))
    if not os.path.exists(savedir):
        os.makedirs(savedir)

    browser.get(url_to_process)

    try:
        download_button = browser.find_element_by_xpath(
            '//*[@ng-if="ctrl.excelDownloadUrl"]')
        download_button.click()

        expected_filename = ("serial-publications--" +
                             str(year) + str(month) + str(day) + '-' +
                             str(year) + str(month) + str(day) +
                             ".xlsx")
        while not glob.glob(temp_down_dir + expected_filename):
            time.sleep(1)
            print("   Waiting 1 sec for download to finish...")

        orig_file = temp_down_dir + expected_filename
        new_filename = (savedir + "/" + material_type +
                        '-' + url_date + ".xlsx")
        os.rename(orig_file, new_filename)

        new_csv_filename = (savedir + "/" + material_type +
                            '-' + url_date + ".csv")
        csv_from_excel(new_filename,
                       new_csv_filename)

    except NoSuchElementException:
        print("   No Results!")
        empty_date_filename = savedir + "/" + material_type + "_empty.txt"
        with open(empty_date_filename, 'w') as emptyfile:
            emptyfile.write("no hits for this date!")


def get_elapsed_time_str(start_time):
    elapsed_time = int(time.time() - start_time)
    sensible_elapsed_time = str(
        datetime.timedelta(seconds=elapsed_time))
    return(sensible_elapsed_time)


def get_start_params(argv):
    start_date = '1911-01-01'
    end_date = '1920-01-01'
    material_type = 'journals'
    output_dir = 'output/test/'

    try:
        opts, args = getopt.getopt(argv, "",
                                   ["start_date=",
                                    "end_date=",
                                    "material_type=",
                                    "output_dir="]
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
        elif opt == "--output_dir":
            output_dir = arg

    return(start_date, end_date, material_type, output_dir)


start_time = time.time()
display = Display(visible=0, size=(800, 600))
display.start()


# year_list = list(range(1911, 1912))
# month_list = list(range(1, 13))


temp_down_dir = 'download_temp/'
downdir = os.path.join(os.getcwd(), temp_down_dir)


prefs = {'download.default_directory': downdir}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.implicitly_wait(60)
browser.set_window_size(800, 600)


(start_date,
 end_date,
 material_type,
 output_dir) = get_start_params(sys.argv[1:])

print("Scraping from " + start_date + " to " + end_date)
start_datetime = get_datetime_from_arg(start_date)
end_datetime = get_datetime_from_arg(end_date)
scraping_datetime = start_datetime


while scraping_datetime <= end_datetime:
    print("Scraping date: " + str(scraping_datetime))
    fetch_csv_for_day(year=scraping_datetime.year,
                      month=scraping_datetime.month,
                      day=scraping_datetime.day,
                      browser=browser,
                      material_type=material_type,
                      output_dir=output_dir)
    print("   " + get_elapsed_time_str(start_time) + " -> done.")
    seconds = random.random() * 5
    time.sleep(seconds)
    scraping_datetime = scraping_datetime + datetime.timedelta(days=1)

# for year in year_list:
#     for month in month_list:
#         day_list = get_daylist_for_month(year, month)
#         for day in day_list:
#             seconds = random.random() * 5
#             time.sleep(seconds)
#             month_str = convert_day_or_month_to_str(month)
#             timestamp_str = '-'.join([str(year), month_str, day])
#             print("Scraping date: " + timestamp_str)
#             fetch_csv_for_day(year, month_str, day, browser,
#                               material_type='journals',
#                               output_dir='output/test/')
#             print("   " + get_elapsed_time_str(start_time) + " -> done.")

print("")
print("----------------------------------------------")
print("   All done in " + get_elapsed_time_str(start_time))
print("----------------------------------------------")


browser.quit()
display.stop()

# usage:
#  python digi_selenium_scraper_xls.py --start_date 1911-01-01 --end_date 1920-12-31 --material_type journals --output_dir output/scrape_results/
