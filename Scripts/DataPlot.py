import numpy as np
import datetime
from os import listdir
import matplotlib.pyplot as plt
import math
import imageio
import os,sys
import time
#<-------------Funcion para obtener el numero de grillas------------->
def delimiter(lon,dg):
    dlon=int(math.ceil(abs(lon[1]-lon[0])/dg))
    return dlon
#<--------------Funcion para obtener el dia,mes y año a partir del dia consecutivo--------->
def date(days):
    date=datetime.date(2020,1,1)+datetime.timedelta(days=days)
    year=date.year
    month=date.month
    day=date.day
    return year,month,day
#<------------------------Funcion para generar el gif---------------------------->
def create_gif(filenames, duration):
	images = []
	for filename in filenames:
		images.append(imageio.imread(filename))
	output_file='../Graphics/Fire.gif'
	imageio.mimsave(output_file, images, duration=duration)
#<---------------------Funcion para trasladar las posiciones--------------------->
def tras(lon,lat,lon_i,lat_i,fig_x,fig_y,n):
    lon,lon_i=redef(lon,lon_i,fig_x,n)
    lat,lat_i=redef(lat,lat_i,fig_y,n)
    return lon,lat,lon_i,lat_i
#<------------------------Funcion para redefinir las posiciones--------------------->
def redef(lon,lon_i,fig_x,n):
    lon_p=lon_i[0]
    for i in range(n):
        lon[i]=(lon[i]+abs(lon_p))*fig_x
    for i in range(2):
        lon_i[i]=(lon_i[i]+abs(lon_p))*fig_x
    if lon_i[0]>lon_i[1]:
        aux=lon_i[1]
        lon_i[1]=lon_i[0]
        lon_i[0]=aux
    return lon,lon_i
#<--------------------Localizacion de los datos----------------------->
dir="../FIRMS/viirs/South_America/" 
#<----------------------Dimensiones de la imagen-------------------->
fig_x,fig_y=360.5,358.5
files=listdir(dir);files=np.sort(files)
#<-------------------------Lectura de la imagen------------------->
map=plt.imread("../Graphics/map2.png")
month_name=["Junio","Julio","Agosto"]
n_data=np.size(files)
sum_t=np.zeros(n_data);date_data=[]
k=0
for file in files:
    lat,lon=np.loadtxt(dir+file,delimiter=",",skiprows=1,usecols=[0,1],unpack=True)
    #<------------------------Valores iniciales de la localizacion------------------->
    lon_i=[-61,-60];lat_i=[-33.5,-32.5];dg=0.25
    n_dlon=delimiter(lon_i,dg);n_dlat=delimiter(lat_i,dg)
    day=int(file[42:45])-1
    year,month,days=date(day)
    n=np.size(lat)
    count=np.zeros([n_dlon,n_dlat],dtype=int)
    for dlon in range(n_dlon):
        r_lon=lon_i[0]+(dlon+1)*dg
        for dlat in range(n_dlat):
            r_lat=lat_i[0]+(dlat+1)*dg
            for i in range(n):
                #<------------------Conteo de los puntos---------------------->
                if r_lat-dg<lat[i]<r_lat and r_lon-dg<lon[i]<r_lon:
                    count[dlon,dlat]+=1
    sum=np.sum(count)
    if k!=0:
        sum_t[k]=sum_t[k-1]+sum
    else:
        sum_t[k]=sum
    if k%5==0:
        date_data=np.append(date_data,str(days)+"-"+month_name[month-6])
    k+=1
    #<-------------------Traslacion de los puntos------------------------------->
    lon,lat,lon_i,lat_i=tras(lon,lat,lon_i,lat_i,fig_x,fig_y,n)
    for dlon in range(n_dlon):
        #<-------------------------Localizacion en x-------------------------->
        r_lon=lon_i[0]+(dlon+1)*dg*fig_x-dg*fig_x/1.7
        for dlat in range(n_dlat):
            #<-------------------------Localizacion en y-------------------------->
            r_lat=lat_i[0]+(dlat+1)*dg*fig_y-dg*fig_y/1.7
            if count[dlon,dlat]!=0:
                #<--------------------------Ploteo del texto-------------------------->
                plt.text(r_lon,r_lat,str(count[dlon,dlat]),fontsize=12,color="black")
    plt.grid(color="black",ls="--")
    lon_i2=[-61,-60];lat_i2=[-33.5,-32.5]
    plt.xlabel("Longitud");plt.ylabel("Latitud ")
    #<-------------------------------Ploteo del mapa------------------------------>
    plt.imshow(map)
    plt.title("Day "+str(days)+"-"+str(month)+"-"+str(year)+"\n Total de incendios: "+str(sum))
    #<--------------------------------Ploteo de los puntos-------------------------->
    plt.scatter(lon,lat,alpha=0.25,color="red",marker=".")
    plt.xticks(np.arange(0,fig_x*(5/4),fig_x/4),np.arange(lon_i2[0],lon_i2[1]+dg,dg))
    plt.yticks(np.arange(0,fig_y*(5/4),fig_y/4),np.arange(lat_i2[0],lat_i2[1]+dg,dg))
    plt.xlim(lon_i[0],lon_i[1])
    plt.ylim(lat_i[0],lat_i[1])
    plt.savefig(str(day)+".png")
    plt.clf()
script = sys.argv.pop(0)
duration = 0.5
filenames = sorted(filter(os.path.isfile, [x for x in os.listdir() if x.endswith(".png")]), key=lambda p: os.path.exists(p) and os.stat(p).st_mtime or time.mktime(datetime.now().timetuple()))
create_gif(filenames, duration)
os.system("rm *.png")
plt.subplots_adjust(left=0.125,right=0.9,bottom=0.183,top=0.92)
plt.plot(np.arange(n_data),sum_t,color="red")
plt.ylabel("Número de incendios acumulados")
plt.xticks(np.arange(0,n_data,5),date_data,rotation=90)
plt.ylim(0,5500)
plt.yticks(np.arange(0,6200+500,500))
plt.grid(ls="--")
plt.savefig("../Graphics/NIA.png")