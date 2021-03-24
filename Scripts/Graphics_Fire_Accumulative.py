import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def dates_ticks(data, day_separation):
    """
    Función que prepara dos arrays para renombrar las
    etiquetas del eje x de la grafica con las fechas
    """
    # Longitud de datos
    data_len = data["Dates"].count()
    # Separación de fechas a imprimir
    loc = np.arange(0,
                    data_len,
                    day_separation)
    # Si no se encuentra la ultima fecha agregarla
    if data["Dates"][loc[-1]] != data["Dates"][data_len-1]:
        loc = np.append(loc, data_len-1)
    # Obtener las fechas seleccionadas
    dates = list(data["Dates"][loc])
    return loc, dates


inputs = {
    "path data": "../Archivos/",
    "path graphics": "../Graphics/",
    "city": "Parana",
    "Days separation": 7,
}
# Lectura de los datos
data = pd.read_csv(inputs["path data"]+inputs["city"]+"/NI.csv")
data["NIA"] = data["NI"][0]
for i in range(1, len(data.index)):
    data["NIA"][i] = data["NI"][i]+data["NIA"][i-1]
# Formato de la fecha en Dia-Nombre del mes
data["Dates"] = pd.to_datetime(data["Dates"]).dt.strftime("%d-%b")
# Extraccion de las fechas seleccionadas
days, dates = dates_ticks(data,
                          inputs["Days separation"])
# Limites de las graficas
plt.subplots_adjust(left=0.121,
                    right=0.952,
                    bottom=0.162,
                    top=0.924)
# Ploteo de los datos
plt.plot(list(data.index), list(data["NIA"]),
         color="#9a031e",
         alpha=0.5)
plt.scatter(data.index, list(data["NIA"]),
            marker=".",
            c="#9a031e",
            alpha=0.5)
# Limites de las graficas
plt.xlim(days[0], days[-1]+1)
plt.ylim(0, 13500)
# Etiqueta en el eje y
plt.ylabel("Número de Incendios")
# Cambio en las etiquetas de los ejes x y y
plt.xticks(days, dates,
           rotation=45)
plt.yticks(np.arange(0, 13500+750, 750))
# Creación del grid
plt.grid(ls="--",
         color="grey",
         alpha=0.7)
# Guardado de la grafica
plt.savefig(inputs["path graphics"]+inputs["city"]+"/Fire_Accumulative.png")
