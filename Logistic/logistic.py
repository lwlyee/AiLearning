#coding=utf-8
import sys
import math
from matplotlib import pyplot as plt
import numpy as np

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
        valueMat.append([1.0, float(tempStr[0]), float(tempStr[0])])
        typeMat.append(int(tempStr[2]))
        line = f.readline()
    f.close()
    valueMat = np.mat(valueMat)
    typeMat = np.mat(typeMat).transpose()
    return valueMat, typeMat

def sigmoid(num):
    return 1/(1.0 + np.exp(-num))

def logistic(fname):
    valueMat, typeMat = loadData(fname)
    m, n = np.shape(valueMat)
    stepSize = 0.001
    times = 300
    weights = np.ones((n, 1))
    for i in range(times):
        prediction = sigmoid(valueMat*weights)
        error = (typeMat - prediction)
        weights = weights + stepSize * valueMat.transpose() * error
    print(weights)
    return weights

logistic(sys.argv[1])