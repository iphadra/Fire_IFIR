import numpy as np
import datetime
from os import listdir
import matplotlib.pyplot as plt
import math
import imageio
import os,sys
import time
def delimiter(lon,dg):
    dlon=int(math.ceil(abs(lon[1]-lon[0])/dg))
    return dlon
def date(days):
    date=datetime.date(2020,1,1)+datetime.timedelta(days=days)
    year=date.year
    month=date.month
    day=date.day
    return year,month,day
#Funcion para generar el gif
def create_gif(filenames, duration):
	images = []
	for filename in filenames:
		images.append(imageio.imread(filename))
	output_file='Animation.gif'
	imageio.mimsave(output_file, images, duration=duration)
def tras(lon,lat,lon_i,lat_i,fig_x,fig_y,n):
    lat_p=lat_i[0]
    lon_p=lon_i[0]
    for i in range(n):
        lat[i]=(lat[i]+abs(lat_p))*fig_y
        lon[i]=(lon[i]+abs(lon_p))*fig_x
    for i in range(2):
        lat_i[i]=(lat_i[i]+abs(lat_p))*fig_y
        lon_i[i]=(lon_i[i]+abs(lon_p))*fig_x
    if lon_i[0]>lon_i[1]:
        aux=lon_i[1]
        lon_i[1]=lon_i[0]
        lon_i[0]=aux
    if lat_i[0]>lat_i[1]:
        aux=lat_i[1]
        lat_i[1]=lat_i[0]
        lat_i[0]=aux
    return lon,lat,lon_i,lat_i
dir="../FIRMS/viirs/South_America/" 
fig_x,fig_y=360.5,358.5
files=listdir(dir);files=np.sort(files)
map=plt.imread("../Graphics/map2.png")
for file in files:
    lat,lon=np.loadtxt(dir+file,delimiter=",",skiprows=1,usecols=[0,1],unpack=True)
    lon_i=[-61,-60];lat_i=[-33.5,-32.5];dg=0.25
    n_dlon=delimiter(lon_i,dg);n_dlat=delimiter(lat_i,dg)
    day=int(file[42:45])
    year,month,days=date(day)
    print(year,month,days)
    n=np.size(lat)
    count=np.zeros([n_dlon,n_dlat],dtype=int)
    delete=0
    for dlon in range(n_dlon):
        r_lon=lon_i[0]+(dlon+1)*dg
        for dlat in range(n_dlat):
            r_lat=lat_i[0]+(dlat+1)*dg
            for i in range(n):
                if r_lat-dg<lat[i]<r_lat and r_lon-dg<lon[i]<r_lon:
                    count[dlon,dlat]+=1
    lon,lat,lon_i,lat_i=tras(lon,lat,lon_i,lat_i,fig_x,fig_y,n)
    plt.title("Day "+str(days)+"-"+str(month)+"-"+str(year))
    plt.scatter(lon,lat,alpha=0.25,color="red",marker=".")
    dg_x=dg*fig_x
    dg_y=dg*fig_y
    for dlon in range(n_dlon):
        r_lon=lon_i[0]+(dlon+1)*dg_x-dg_x/1.7
        for dlat in range(n_dlat):
            r_lat=lat_i[0]+(dlat+1)*dg_y-dg_y/1.7
            if count[dlon,dlat]!=0:
                plt.text(r_lon,r_lat,str(count[dlon,dlat]),fontsize=12,color="black")
    plt.grid(color="black")
    lon_i2=[-61,-60];lat_i2=[-33.5,-32.5];dg=0.25
    plt.xlabel("Longitud")
    plt.ylabel("Latitud ")
    plt.imshow(map)
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