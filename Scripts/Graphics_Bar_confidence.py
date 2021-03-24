import matplotlib.pyplot as plt
import pandas as pd
import os


def autolabel(ax, rects):
    """
    Funcion que grafica los valores de cada barra
    """
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',)


inputs = {
    "path data": "../Archivos/",
    "path graphics": "../Graphics/",
    "Confidence names": ["low", "nominal", "high"],
    "City": "Parana/",
}
path = inputs["path data"]+inputs["City"] + "Dates_data/"
data_count = pd.DataFrame(columns=inputs["Confidence names"], data=[[0, 0, 0]])
files = sorted(os.listdir(path))
for file in files:
    data = pd.read_csv(path+file)
    count = data.groupby("Confidence").count()
    for confidence_name in inputs["Confidence names"]:
        try:
            data_count[confidence_name] += count["Longitude"][confidence_name]
        except KeyError:
            pass
total = data_count.sum(axis=1)[0]
data_count = data_count*100/total
data_percentage = [data_count[data][0] for data in data_count]
fig, ax = plt.subplots()
rect = ax.bar(inputs["Confidence names"], data_percentage, 0.75)
autolabel(ax, rect)
rect[0].set_color("#22577a")
rect[1].set_color("#38a3a5")
rect[2].set_color("#57cc99")
ax.set_ylim(0, 90)
ax.set_ylabel("Frecuencia de intervalo de confianza (%)")
ax.set_xlabel("nivel de confianza")
plt.savefig(inputs["path graphics"]+inputs["City"] +
            "/Bar_confidence_percentage.png")
