import xlrd
import csv
from calendar import monthrange
import datetime


def convert_day_or_month_to_str(day):
    if day < 10:
        day_str = '0' + str(day)
    else:
        day_str = str(day)
    return day_str


def csv_from_excel(xlsx_file, csv_file):
    wb = xlrd.open_workbook(xlsx_file)
    sh = wb.sheet_by_name('Tulokset')
    with open(csv_file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for rownum in range(sh.nrows):
            csvwriter.writerow(sh.row_values(rownum))


def convert_day_or_month_range_to_str(days_range):
    days_range_str = []
    for day in days_range:
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)
        days_range_str.append(day)
    return days_range_str


def get_daylist_for_month(year, month):
    days_in_month = monthrange(year, month)[1]
    days_range = list(range(1, (days_in_month + 1)))
    days_range_str = convert_day_or_month_range_to_str(days_range)
    return days_range_str


def get_datetime_from_arg(arg_date):
    # arg_date format: '1911-01-01' YYYY-MM-DD
    arg_date_list = arg_date.split('-')
    start_year = int(arg_date_list[0])
    start_month = int(arg_date_list[1])
    start_day = int(arg_date_list[2])
    arg_datetime = datetime.date(start_year, start_month, start_day)
    return(arg_datetime)
