#coding=utf-8
import sys
import numpy as np
from matplotlib import pyplot as plt

color = ['blue', 'green', 'red', 'yellow', 'black', 'magenta', 'cyan']
plt.xlabel("x")
plt.ylabel("y")

def loadData(fname, type):
    if type == 'p':
        x, y, type = np.loadtxt(fname, delimiter=',', comments='#', unpack=True, encoding='utf-8')
        print(type)
        print(type[0])
        return x, y, type
    elif type == 't':
        x, y = np.loadtxt(fname, delimiter=',', comments='#', unpack=True, encoding='utf-8')
        return x, y

def findDistance(x, y, pointX, pointY):
    return(list(map(lambda tempx, tempy: ((x - tempx)**2 + (y - tempy)**2)**0.5, pointX, pointY)))

def countMax(list,p_typeValue):
    temp = 0
    value = ''
    for i in range(len(p_typeValue)):
        if list.count(p_typeValue[i]) > temp:
            temp = list.count(p_typeValue[i])
            value = p_typeValue[i]
    return value

def KNN(pFile, tFile, k):
    type = []
    t_type = []
    p_typeSet = set()
    p_x, p_y, p_type = loadData(pFile, 'p')
    t_x, t_y = loadData(tFile, 't')
    for i in range(len(p_type)):
        p_typeSet.add(p_type[i])
        p_typeValue = list(p_typeSet)
    for i in range(len(t_x)):
        distance = findDistance(t_x[i], t_y[i], p_x, p_y)
        tempDistance = distance[:]
        tempDistance.sort(reverse=False)
        tempDistance = tempDistance[0:k]
        type.clear()
        for j in range(len(tempDistance)):
            type.append(p_type[distance.index(tempDistance[j])])
        t_type.append(countMax(type, p_typeValue))
        plt.scatter(t_x[i], t_y[i], marker='x', color=color[p_typeValue.index(t_type[i])])
    for i in range(len(p_x)):
        plt.scatter(p_x[i], p_y[i], marker='o', color=color[p_typeValue.index(p_type[i])])
    plt.show()

KNN(sys.argv[1], sys.argv[2], int(sys.argv[3]))