import matplotlib.pyplot as plt
import numpy as np

def plot_points(lon,lat):
    plt.scatter(lon, lat, alpha=0.25, color="red", marker=".")

def plot_map(map,date,sum,lon_list,lat_list,lon_tras,lat_tras,name,path=""):
    plt.xlabel("Longitud");plt.ylabel("Latitud ")
    # <-------------------------------Ploteo del mapa------------------------------>
    plt.imshow(map)
    plt.title("Day "+date+"\n Total de incendios: "+str(sum))
    # <--------------------------------Ploteo de los puntos--------------------------
    plt.xticks(lon_tras,lon_list)
    plt.yticks(lat_tras,lat_list)
    plt.xlim(lon_tras[0], lon_tras[-1])
    plt.ylim(lat_tras[0], lat_tras[-1])
    plt.grid(color="black", ls="--")
    plt.savefig(path+name+".png")
    plt.clf()

def number_plot(lon_list,lat_list,count_list):
    lon_n=np.size(lon_list)
    lat_n=np.size(lat_list)
    for lon_i,counts in zip(range(lon_n-1),count_list):
        #<-------------------------Localizacion en x-------------------------->
        r_lon=(lon_list[lon_i+1]+lon_list[lon_i])/2
        for lat_i,count in zip(range(lat_n-1),counts):
            #<-------------------------Localizacion en y-------------------------->
            r_lat=(lat_list[lat_i+1]+lat_list[lat_i])/2
            if count!=0:
                #<--------------------------Ploteo del texto-------------------------->
                plt.text(r_lon,r_lat,str(count),fontsize=12,color="black")
