#coding=utf-8
import sys
import numpy as np
from matplotlib import pyplot as plt

color = ['blue', 'green', 'red', 'yellow', 'black', 'magenta', 'cyan']
plt.xlabel("x")
plt.ylabel("y")

def loadData(fname):
    valueMat = [];typeMat = []
    f = open(fname, mode='r', encoding='utf-8')
    next(f)
    line = f.readline()
    while line:
        line = line.replace('\n', '')
        tempStr = line.split(',')
        valueMat.append([1.0, float(tempStr[0]), float(tempStr[1])])
        typeMat.append(int(tempStr[2]))
        plt.scatter(float(tempStr[0]), float(tempStr[1]), color=color[int(tempStr[2])])
        line = f.readline()
    f.close()
    valueMat = np.mat(valueMat)
    typeMat = np.mat(typeMat).transpose()
    print(valueMat, typeMat)
    return valueMat, typeMat

loadData('data.txt')