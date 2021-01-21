import matplotlib.pyplot as plt
import numpy as np
import datetime
#<--------------Funcion para obtener el dia,mes y año a partir del dia consecutivo--------->
def conse_date(names,days):
    date=datetime.date(2020,1,1)+datetime.timedelta(days=days)
    day=date.day
    if day<10:
        day="0"+str(day)
    else:
        day=str(day)
    month=date.month
    date=day+"-"+names[month-6]
    return date
dir_files="../Archivos/";dir_Graphics="../Graphics/"
month_names=["Jun","Jul","Ag","Sept"]
days,n_day=np.loadtxt(dir_files+"suomiNIA.txt",unpack=True)
dates=[]
div=np.arange(0,np.size(days),6)
if days[div[-1]]!=days[-1]:
    div=np.append(div,-1)
for day in days:
    dates=np.append(dates,conse_date(month_names,day))
plt.subplots_adjust(left=0.121,right=0.952,bottom=0.162,top=0.924)
plt.scatter(days,n_day,marker=".",c="#9a031e",alpha=0.5)
plt.plot(days,n_day,color="#9a031e")
plt.ylim(0,550)
plt.ylabel("Número de Incendios")
plt.xlim(days[0],days[-1]+1)
plt.yticks(np.arange(0,600,50))
plt.xticks(days[div],dates[div],rotation=90)
plt.grid(ls="--",color="grey",alpha=0.7)
plt.savefig(dir_Graphics+"Fire_Day.png")