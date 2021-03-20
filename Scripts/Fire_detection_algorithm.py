import matplotlib.pyplot as plt
import moviepy.editor as mp
from functions import *
import pandas as pd
import numpy as np
import imageio


class Fire:
    def __init__(self, day_initial, day_final, fig_x, fig_y, lon, lat, delta):
        self.day_initial = day_initial
        self.day_final = day_final
        self.fig_x = fig_x
        self.fig_y = fig_y
        self.lon = lon
        self.lat = lat
        self.delta = delta
        self.conf_names = ["low", "nominal", "high"]
        self.conf_count = np.zeros(3)
        self.create_grids()

    def create_grids(self):
        self.lon_division, self.lon_n = self.delimiter_grids(self.lon,
                                                             self.delta)
        self.lat_division, self.lat_n = self.delimiter_grids(self.lat,
                                                             self.delta)
        self.lon_division_tras = self.traslation_positions(self.lon_division,
                                                           self.lon,
                                                           self.fig_x)
        self.lat_division_tras = self.traslation_positions(self.lat_division,
                                                           self.lat,
                                                           self.fig_y)

    def delimiter_grids(self, pos_points, delta):
        """
        Funcion para obtener el numero de grillas
        """
        pos = np.arange(pos_points[0], pos_points[1]+delta, delta)
        size = np.size(pos)
        return pos, size

    def traslation_positions(self, pos_data, pos_parameter, resize):
        """
        Funcion para redefinir las posicioness
        """
        n = np.size(pos_data)
        pos_data_tras = np.zeros(n)
        for i in range(n):
            pos_data_tras[i] = (pos_data[i]-pos_parameter[0])*resize
        return pos_data_tras

    def read_filenames(self, path):
        self.files = sorted(os.listdir(path))

    def read_map(self, path, name):
        self.map = plt.imread(path+name)

    def algorithm(self, path_data, path_results, path_graphics):
        print("Realizando conteo de incendios")
        results_file = open(path_results+"NIA2.csv", "w")
        for file in self.files:
            self.data = self.read_data_from_each_file(file, path_data)
            year, conse_day = self.obtain_date_from_name(file)
            self.date = str(consecutiveday2date(conse_day, year))
            if self.day_initial <= self.date <= self.day_final:
                self.count_fire()
                sum = np.sum(self.count)
                results_file.write("{},{}\n".format(self.date, sum))
                lat = np.array(self.data["latitude"])
                lon = np.array(self.data["longitude"])
                lon = self.traslation_positions(lon, self.lon, self.fig_x)
                lat = self.traslation_positions(lat, self.lat, self.fig_y)
                self.number_plot(self.lon_division_tras,
                                 self.lat_division_tras,
                                 self.count)
                self.plot_points(lon, lat)
                self.plot_map(sum, self.date, path_graphics)
        results_file.close()

    def count_fire(self):
        self.count = np.zeros([self.lon_n, self.lat_n], dtype=int)
        data_size = np.size(self.data["latitude"])
        for lon_i in range(self.lon_n-1):
            lon_initial = self.lon_division[lon_i]
            lon_final = self.lon_division[lon_i+1]
            for lat_i in range(self.lat_n-1):
                lat_initial = self.lat_division[lat_i]
                lat_final = self.lat_division[lat_i+1]
                for data_i in range(data_size):
                    # <------------------Conteo de los puntos---------------------->
                    lon_decision = lon_initial < self.data["longitude"][data_i] < lon_final
                    lat_decision = lat_initial < self.data["latitude"][data_i] < lat_final
                    if lon_decision and lat_decision:
                        if self.data["confidence"][data_i] == "nominal":
                            self.count[lon_i, lat_i] += 1
                        # for j in range(3):
                        #     self.conf_count[j] = np.size(
                        #         conf[conf == conf_names[j]])

    def read_data_from_each_file(self, name, path):
        data = pd.read_csv(path+name, usecols=[0, 1, 8])
        return data

    def obtain_date_from_name(self, name):
        date = name.split("_")[7]
        year = int(date[0:4])
        conse_day = int(date[4:7])-1
        return year, conse_day

    def plot_points(self, lon, lat):
        plt.scatter(lon, lat, alpha=0.25, color="red", marker=".")

    def plot_map(self, sum, name, path=""):
        plt.xlabel("Longitud")
        plt.ylabel("Latitud ")
        # <-------------------------------Ploteo del mapa------------------------------>
        plt.imshow(self.map)
        plt.title("Date {}\nTotal de incendios: {}".format(self.date, sum))
        # <--------------------------------Ploteo de los puntos--------------------------
        plt.xticks(self.lon_division_tras, self.lon_division)
        plt.yticks(self.lat_division_tras, self.lat_division)
        plt.xlim(self.lon_division_tras[0], self.lon_division_tras[-1])
        plt.ylim(self.lat_division_tras[0], self.lat_division_tras[-1])
        plt.grid(color="black", ls="--")
        plt.savefig(path+name+".png")
        plt.clf()

    def number_plot(self, lon_list, lat_list, count_list):
        lon_n = np.size(lon_list)
        lat_n = np.size(lat_list)
        for lon_i, counts in zip(range(lon_n-1), count_list):
            # <-------------------------Localizacion en x-------------------------->
            r_lon = (lon_list[lon_i+1]+lon_list[lon_i])/2
            for lat_i, count in zip(range(lat_n-1), counts):
                # <-------------------------Localizacion en y-------------------------->
                r_lat = (lat_list[lat_i+1]+lat_list[lat_i])/2
                if count != 0:
                    # <--------------------------Ploteo del texto-------------------------->
                    plt.text(r_lon, r_lat, str(count),
                             fontsize=12, color="black")

    def create_animation(self, path="", name="Fire", duration=0.5, delete=True):
        self.create_gif(path, duration, name, delete)
        self.movie_maker(path, name, delete)

    def create_gif(self, path, duration, name, delete_images):
        print("Creando gif")
        filenames = sorted(os.listdir(path))
        images = []
        for filename in filenames:
            images.append(imageio.imread(path+filename))
        output_file = path+name+'.gif'
        imageio.mimsave(output_file, images, duration=duration)
        if delete_images:
            os.system("rm "+path+"*.png")

    def movie_maker(self, path, name, delete_gif):
        clip = mp.VideoFileClip(path+name+'.gif')
        clip.write_videofile(path+name+".mp4")
        if delete_gif:
            os.system("rm "+path+"*.gif")
