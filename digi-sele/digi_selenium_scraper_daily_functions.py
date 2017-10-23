import csv
import os
import random
import time
import urllib.request
import glob
from digi_selenium_scraper_common_functions import (
    convert_day_or_month_to_str)
import http


def read_csv_to_dictlist(csv_filename, browser):
    with open(csv_filename) as csvfile:
        papers_list = []
        csvreader = csv.reader(csvfile)
        for i in range(2):
            next(csvreader)
        for row in csvreader:
            url = row[6]
            url_common_prefix = url.split('?page=1')[0] + '/'
            binding_no = url_common_prefix.split('/')[5]
            browser.get(url)
            print('processing row with url: ' + url)
            last_page = browser.find_element_by_css_selector(
                'div.page-navigation span.ng-binding').text
            last_page = last_page[1:]
            row_dict = {'binding_no': binding_no,
                        'title': row[0],
                        'issn': row[1],
                        'url': url,
                        'url_common_prefix': url_common_prefix,
                        'last_page': last_page}
            papers_list.append(row_dict)
            # print('processed row with url: ' + url)
    return(papers_list)


def write_refined_csv(day_dir, day_list, material_type):
    y_str = day_dir.split('/')[2]
    m_str = day_dir.split('/')[3]
    d_str = day_dir.split('/')[4]
    new_csv_filename = (day_dir + 'refined_' +
                        material_type + '-' +
                        y_str + '-' +
                        m_str + '-' +
                        d_str + '.csv')

    with open(new_csv_filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['binding_no',
                            'title',
                            'issn',
                            'url',
                            'url_common_prefix',
                            'last_page'])
        for item in day_list:
            csvwriter.writerow([item.get('binding_no'),
                                item.get('title'),
                                item.get('issn'),
                                item.get('url'),
                                item.get('url_common_prefix'),
                                item.get('last_page')])

    print("Wrote refined csv-file for data: " +
          y_str + "/" + m_str + "/" + d_str + " - " + material_type)


def download_items_from_day_list(day_list, day_dir, material_type,
                                 scrape_images=False):
    y_str = day_dir.split('/')[2]
    m_str = day_dir.split('/')[3]
    d_str = day_dir.split('/')[4]
    for item in day_list:
        url_common_prefix = item.get('url_common_prefix')
        item_dir = day_dir + item.get('binding_no')
        last_page = item.get('last_page')

        if not os.path.exists(item_dir):
            os.makedirs(item_dir)

        page_list = list(range(1, int(last_page) + 1))

        print("Getting content for binding: " + item.get('binding_no') +
              " - " + y_str + "/" + m_str + "/" + d_str + "-" +
              material_type + " - pages: " + last_page)

        for page_number in page_list:
            page_str = str(page_number)
            text_url = url_common_prefix + "page-" + page_str + ".txt"
            text_filename = item_dir + '/' + "page-" + page_str + ".txt"
            alto_url = url_common_prefix + "page-" + page_str + ".xml"
            alto_filename = item_dir + '/' + "page-" + page_str + ".xml"
            image_url = url_common_prefix + "image/" + page_str
            image_filename = item_dir + '/' + "page-" + page_str + ".jpg"

            seconds = random.random() * 0.3 + 0.5
            time.sleep(seconds)

            for attempt in range(1, 11):
                try:
                    urllib.request.urlretrieve(text_url,
                                               filename=text_filename)
                    time.sleep(0.1)
                    urllib.request.urlretrieve(alto_url,
                                               filename=alto_filename)
                    if scrape_images:
                        urllib.request.urlretrieve(image_url,
                                                   filename=image_filename)
                    break
                except http.client.HTTPException as e:
                    print(e)
                    print(str(attempt) + "/10 Retrying in 2 seconds.")
                    time.sleep(2)
                    continue
                break


def download_material_for_day(year, month, day, material_type, browser):

    day_dir = ('output/scrape_results/' +
               str(year) + '/' +
               convert_day_or_month_to_str(month) + '/' +
               convert_day_or_month_to_str(day) + '/')
    csv_filename = (day_dir +
                    material_type + '-' +
                    str(year) + '-' +
                    convert_day_or_month_to_str(month) + '-' +
                    convert_day_or_month_to_str(day) + '.csv')

    if not glob.glob(csv_filename):
        print(" ---- no papers to scrape for: " + day_dir)
    else:
        day_list = read_csv_to_dictlist(csv_filename, browser)
        write_refined_csv(day_dir, day_list, material_type)
        download_items_from_day_list(day_list, day_dir, material_type)
