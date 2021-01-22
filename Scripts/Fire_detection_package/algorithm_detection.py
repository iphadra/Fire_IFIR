from .date_formats import *
from .read_data import *
import numpy as np


def count_fire(file, path, lon_division, lat_division, lon_n, lat_n, cont_conf, conf_names, loc_dates):
    lat, lon, conf = read_lat_lot_conf(file, path)
    conse_day = int(file[loc_dates[0]:loc_dates[1]])-1
    year, month, days = consecutive2yymmdd(conse_day)
    count = np.zeros([lon_n, lat_n], dtype=int)
    data_n = np.size(lat)
    for lon_i in range(lon_n-1):
        for lat_i in range(lat_n-1):
            for data_i in range(data_n):
                # <------------------Conteo de los puntos---------------------->
                lon_decision = lon_division[lon_i] < lon[data_i] < lon_division[lon_i+1]
                lat_decision = lat_division[lat_i] < lat[data_i] < lat_division[lat_i+1]
                if lon_decision and lat_decision:
                    if conf[data_i] == "nominal":
                        count[lon_i, lat_i] += 1
                    for j in range(3):
                        cont_conf[j] = np.size(conf[conf == conf_names[j]])
    return lat, lon, conse_day, count, cont_conf
