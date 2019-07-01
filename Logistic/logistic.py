#coding=utf-8
import sys
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
        valueMat.append([1.0, float(tempStr[0]), float(tempStr[1])])
        typeMat.append(int(tempStr[2]))
        plt.scatter(float(tempStr[0]), float(tempStr[1]), color=color[int(tempStr[2])])
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
    times = 9000
    weights = np.ones((n, 1))
    for i in range(times):
        prediction = sigmoid(valueMat*weights)
        error = (typeMat - prediction)
        weights = weights + stepSize * valueMat.transpose() * error
    return weights

weights = logistic(sys.argv[1])
print(weights)
x = np.arange(2, 8, 0.1)
y = ((-weights[0]-weights[1]*x)/weights[2]).reshape(len(x), 1)
plt.plot(x, y, color=color[3])
plt.show()