import datetime
import numpy as np
dir_data = "../Archivos/"
dates, datas = np.loadtxt(dir_data+"suomiNIA.txt", unpack=True, dtype=int)
file = open(dir_data+"suomiNIA.csv", "w")
for date, data in zip(dates, datas):
    day = datetime.date(2020, 1, 1)+datetime.timedelta(days=int(date))
    file.write(str(day)+","+str(data)+"\n")
file.close()
