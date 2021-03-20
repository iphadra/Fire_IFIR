import datetime
import math
import os


def mkdir(name, path=""):
    try:
        os.mkdir(path+name)
    except FileExistsError:
        pass


def format_number(date):
    date = str(date)
    date = "0"*(2-len(date))+date
    return date


def format_date(date):
    date = str(date)
    date = "0"*(2-len(date))+date
    return date


def format_date(date):
    day = format_number(date.day)
    month = format_number(date.month)
    year = str(date.year)[2:4]
    date = year+month+day
    return date


def xlsxdate2date(xldate):
    date = datetime.datetime(1899, 12, 30) + datetime.timedelta(days=xldate)
    date = format_date(date)
    return date


def consecutiveday2date(conse_day, year):
    date = datetime.date(year, 1, 1)+datetime.timedelta(days=conse_day)
    return date


def consecutiveday2yymmdd(conse_day, year):
    date = consecutiveday2date(conse_day, year)
    date = format_date(date)
    return date


def save_measurement(data):
    if float(data) < 0:
        data = 0
    else:
        data = float(data)*1000
    # if data == "":
    #     data = 0
    # if math.isnan(data) == True:
    #     data = 0
    # else:
    #     data = float(data)
    # # Si la medicion es menor a 0, dar el valor de 0
    # if data < 0:
    #     data = 0
    # # Cambios de medicion a W/m^2
    # data = data*1000
    return str(data)


def date2consecutiveday(year, month, day):
    return (datetime.date(year, month, day)-datetime.date(year, 1, 1)).days


def obtain_month(year, year_i, day):
    month = (datetime.date(year+year_i, 1, 1) +
             datetime.timedelta(days=day)).month-1
    return month


def yy_mm_dd2consecutiveday(date, year_i):
    date = date.split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    conse_day = date2consecutiveday(year, month, day)
    days_in_the_middle = (datetime.date(year, 1, 1) -
                          datetime.date(year_i, 1, 1)).days
    conse_day += days_in_the_middle
    return conse_day


def yymmdd2consecutiveday(date, year_i):
    year = int("20"+date[0:2])
    month = int(date[2:4])
    day = int(date[4:6])
    conse_day = date2consecutiveday(year, month, day)
    days_in_the_middle = (datetime.date(year, 1, 1) -
                          datetime.date(year_i, 1, 1)).days
    conse_day += days_in_the_middle
    return conse_day

def yymmdd2yyyy_mm_dd(date):
    year="20"+date[0:2]
    month=date[2:4]
    day=date[4:6]
    date=year+"-"+month+"-"+day
    return date
