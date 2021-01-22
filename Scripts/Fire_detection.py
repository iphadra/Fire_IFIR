from Fire_detection_package import *
import matplotlib.pyplot as plt
import numpy as np
import os
parameters = {
    "data set": "suomi",
    "day part": 5,
    "fig_x": 360.5,
    "fig_y": 358.5,
    "lon": [-61, -60],
    "lat": [-33.5, -32.5],
    "delta": 0.25,
}
# data_sets=["viirs","suomi"]
# loc_dates=[[42,45],[49,52]]

# <---Posicion de los dias consecutivos en los nombres de los archivos----------->
loc_dates = [49, 52]
# <---------------------------Tipos de datos---------------------->
conf_names = ["low", "nominal", "high"]
# <--------------------------Inicializar conteo------------------>
cont_conf = np.zeros(3)
dir_data = "../FIRMS/"+parameters["data set"]+"/South_America/"
dir_results = "../Archivos/"
dir_graphics = "../Graphics/movie/"
# <-------------------------Lectura de la imagen------------------->
map = plt.imread("../Graphics/map2.png")
month_name = ["Jun", "Jul", "Ag", "Sept"]
# <------------Creacion de la grilla de las longitudes y latitudes-------------->
lon_division, lon_n = delimiter(parameters["lon"], parameters["delta"])
lat_division, lat_n = delimiter(parameters["lat"], parameters["delta"])
# <-----Creacion de la grilla de las longitudes y latitudes trasladadas--------->
lon_division_tras = tras(lon_division, parameters["lon"], parameters["fig_x"])
lat_division_tras = tras(lat_division, parameters["lat"], parameters["fig_y"])
files = sorted(os.listdir(dir_data))
n_data = np.size(files)
k = 0
print("Calculando suma de incendios")
NIA_file = open(dir_results+parameters["data set"]+"NIA.csv", "w")
for file in files:
    # <----------Conteo de fuegos en el dia------------------------->
    lat, lon, conse_day, count, cont_conf = count_fire(
        file, dir_data, lon_division, lat_division, lon_n, lat_n, cont_conf, conf_names, loc_dates)
    # <-------------Suma de los fuegos en el dia-------------->
    sum = np.sum(count)
    #<-----------------Escritura de los fuegos en el dia---------->
    NIA_file.write(str(conse_day)+","+str(sum)+"\n")
    # <-------------------Traslacion de los puntos------------------------------->
    lon = tras(lon, parameters["lon"], parameters["fig_x"])
    lat = tras(lat, parameters["lat"], parameters["fig_y"])
    #<---------------------Pĺoteo del numero de fuegos por grilla--------------->
    number_plot(lon_division_tras, lat_division_tras, count)
    #<---------------Extraccion del dia a partir del día consecutivo----------->
    year, month, days = consecutive2yymmdd(conse_day)
    date = str(days)+"-"+str(month)+"-"+str(year)
    name = str(conse_day)
    #<-----------------------Ploteo de los fuegos--------------------->
    plot_points(lon, lat)
    #<--------------------------Ploteo del mapa-------------------->
    plot_map(map, date, sum, lon_division, lat_division,
             lon_division_tras, lat_division_tras, name,path=dir_graphics)
NIA_file.close()
create_gif(path=dir_graphics)
movie_maker(path=dir_graphics)
total = np.sum(cont_conf)
for j in range(3):
    div = round(cont_conf[j]/total*100, 2)
    print(conf_names[j], div)
