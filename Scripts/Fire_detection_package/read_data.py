import numpy as np


def read_lat_lot_conf(name, path):
    lat, lon = np.loadtxt(path+name, delimiter=",",
                          skiprows=1, usecols=[0, 1], unpack=True)
    conf = np.loadtxt(path+name, delimiter=",",
                      skiprows=1, usecols=8, dtype=str)
    return lat, lon, conf
