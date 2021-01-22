import numpy as np
# <------------------------Funcion para redefinir las posiciones--------------------->
def tras(pos_data, pos_parameter, resize):
    n = np.size(pos_data)
    pos_data_tras=np.zeros(n)
    for i in range(n):
        pos_data_tras[i] = (pos_data[i]-pos_parameter[0])*resize
    return pos_data_tras


# <-------------Funcion para obtener el numero de grillas------------->


def delimiter(pos_points, delta):
    pos = np.arange(pos_points[0], pos_points[1]+delta, delta)
    size = np.size(pos)
    return pos, size
