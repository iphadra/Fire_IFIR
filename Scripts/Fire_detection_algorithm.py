import matplotlib.pyplot as plt
import moviepy.editor as mp
from functions import *
import pandas as pd
import numpy as np
import imageio


class Fire:
    def __init__(self, path_data, city, day_initial, day_final, fig_x, fig_y, lon, lat, delta):
        """
        Constructor de la clase Fire, la cual contiene el proceso de conteo de alertas y creacion
        de la animacion.
        Describcion de las variables:
        path_data --> Direccion donde se encuentran los datos recabados del FIRMS
        city -------> Ciudad o zona donde se estara estudiando, es necesaria para guardar los datos en sub carpetas 
        day_initial > Dia de inicio del analisis
        day_final --> Dia de fin del analisis
        fig_x ------> Tamaño en pixeles del mapa en el eje x
        fig_y ------> Tamaño en pixeles del mapa en el eje y
        lon --------> Lista con el valor maximo y minimo de la longitud de la zona de estudio
        lat --------> Lista con el valor maximo y minimo de la latitud de la zona de estudio
        delta ------> Diferencia entre las grillas de la busqueda
        """
        self.path_data = path_data
        self.city = city
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
        """
        Funcion que crea las grillas de biusqueda y realiza la transformacion para el espacio de la imagen
        """
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

    def read_filenames(self):
        """
        Lectura del nombre de los archivos del FIRMS
        """
        self.files = sorted(os.listdir(self.path_data))

    def read_map(self, path, name):
        """
        Lectura del mapa de la zona donde se esta realizando el estudio
        """
        self.map = plt.imread(path+self.city+"/"+name)

    def algorithm(self, path_results, path_graphics):
        """
        Funcion que realiza el algoritmo de conteo en los distintos archivos e FIRMS y dos formatos de archivos
        NI.csv -----> Conteo de los incencos para distintas fechas
        date.csv ---> Existe un archivo diferente para cada fecha, este contiene la localizacion de cada incendio
        """
        # Dirección donde se creara la animacion
        self.path_movie = path_graphics+self.city+"/Movie/"
        print("Realizando conteo de incendios")
        # Archivo NI
        results_file = open(path_results+self.city+"/NI.csv", "w")
        results_file.write("Dates,NIA\n")
        for file in self.files:
            # Lectura de los datos FIRMS
            self.data = self.read_data_from_each_file(file, self.path_data)
            # Extraccion del año y dia consecutivo a partir del nombre del archivo
            year, conse_day = self.obtain_date_from_name(file)
            # Formato de la fecha de la forma yyyy-mm-dd
            self.date = str(consecutiveday2date(conse_day, year))
            # Discriminación para tomar en cuenta el rango de fechas dado
            if self.day_initial <= self.date <= self.day_final:
                # Conteo de los incendios para cada grilla
                self.count_fire(path_results)
                # Conteo de los incendios para todo el dia
                sum = np.sum(self.count)
                # Escritura de los resultados
                results_file.write("{},{}\n".format(self.date, sum))
                # Lectura de la latitud y longitud
                lat = np.array(self.data["latitude"])
                lon = np.array(self.data["longitude"])
                # Traslacion de las cordenadas hacia el espacio de la imagen
                lon = self.traslation_positions(lon, self.lon, self.fig_x)
                lat = self.traslation_positions(lat, self.lat, self.fig_y)
                # Ploteo del numero de incendios por grilla
                self.number_plot(self.lon_division_tras,
                                 self.lat_division_tras,
                                 self.count)
                # Ploteo de cada incendio
                self.plot_points(lon, lat)
                # Ploteo del mapa
                self.plot_map(sum, self.date, self.path_movie)
        results_file.close()

    def count_fire(self, path):
        """
        Algoritmo para el conteo de los incendios en cada grilla
        """
        # Archivo date.csv
        daily_points_file = open(
            path+self.city+"/Dates_data/"+self.date+".csv", "w")
        daily_points_file.write("Longitude,Latitude,Confidence\n")
        # Inicializacion del conteo
        self.count = np.zeros([self.lon_n, self.lat_n], dtype=int)
        # Longitud de los datos
        data_size = np.size(self.data["latitude"])
        for lon_i in range(self.lon_n-1):
            # Limites de la grilla en la longitud
            lon_initial = self.lon_division[lon_i]
            lon_final = self.lon_division[lon_i+1]
            for lat_i in range(self.lat_n-1):
                # Limites de la grilla en la latitud
                lat_initial = self.lat_division[lat_i]
                lat_final = self.lat_division[lat_i+1]
                # Recorrido por todos los datos
                for data_i in range(data_size):
                    # Localizacion de los datos a partir de su longitud
                    lon_decision = lon_initial < self.data["longitude"][data_i] < lon_final
                    # Localizacion de los datos a partir de su latitud
                    lat_decision = lat_initial < self.data["latitude"][data_i] < lat_final
                    # Si esta en la grilla entonces lo contara
                    if lon_decision and lat_decision:
                        # Escritura de los puntos en el archivo para cada día
                        daily_points_file.write("{:.5f},{:.5f},{}\n".format(self.data["longitude"][data_i],
                                                                            self.data["latitude"][data_i],
                                                                            self.data["confidence"][data_i]))
                        if self.data["confidence"][data_i] == "nominal":
                            self.count[lon_i, lat_i] += 1
                        # for j in range(3):
                        #     self.conf_count[j] = np.size(
                        #         conf[conf == conf_names[j]])
        daily_points_file.close()

    def read_data_from_each_file(self, name, path):
        """
        Funcion para la lectura de los datos de FIRMS
        """
        data = pd.read_csv(path+name, usecols=[0, 1, 8])
        return data

    def obtain_date_from_name(self, name):
        """
        Funcion para obtener la fecha a partir del nombre de los archivos de FIRMS
        """
        date = name.split("_")[7]
        year = int(date[0:4])
        conse_day = int(date[4:7])-1
        return year, conse_day

    def plot_points(self, lon, lat):
        """
        Funcion para plotear los puntos de cada incendio
        """
        plt.scatter(lon, lat, alpha=0.25, color="red", marker=".")

    def plot_map(self, sum, name, path=""):
        """
        Funcion para plotear el mapa y guardar la grafica
        """
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
        """
        Funcion para plotear el numero de incendios, si este es 0, no ploteara nada
        """
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

    def create_animation(self, name="Fire", duration=0.5, delete=True):
        """
        Funcion que ejecuta la creacion de la animacion
        """
        self.create_gif(self.path_movie, duration, name, delete)
        self.movie_maker(self.path_movie, name, delete)

    def create_gif(self, path, duration, name, delete_images):
        """
        Funcion que crea el gif a partir de las graficas diarias
        """
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
        """
        Funcion que crea el mp4 a partir del gifs
        """
        clip = mp.VideoFileClip(path+name+'.gif')
        clip.write_videofile(path+name+".mp4")
        if delete_gif:
            os.system("rm "+path+"*.gif")
