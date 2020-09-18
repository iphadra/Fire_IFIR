import matplotlib.pyplot as plt
import numpy as np
#<------------------------Funcion que grafica los valores de cada barra------------->
def autolabel(ax,rects):
    for rect in rects:
        height =round(rect.get_height(),2)
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0,3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',)
values=[4.91,83.74,11.35]
conf_names=["low","nominal","high"]
fig, ax = plt.subplots()
rect=ax.bar(conf_names,values,0.75)
autolabel(ax,rect)
rect[0].set_color("#22577a")
rect[1].set_color("#38a3a5")
rect[2].set_color("#57cc99")
ax.set_ylim(0,90)
ax.set_ylabel("Frecuencia de intervalo de confianza (%)")
ax.set_xlabel("nivel de confianza")
plt.savefig("../Graphics/Bar_Graphic.png")