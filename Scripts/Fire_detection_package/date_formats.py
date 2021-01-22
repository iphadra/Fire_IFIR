# <--------------Funcion para obtener el dia,mes y año a partir del dia consecutivo--------->
import datetime


def consecutive2yymmdd(days):
    date = datetime.date(2020, 1, 1)+datetime.timedelta(days=days)
    year = date.year
    month = date.month
    day = date.day
    return year, month, day
