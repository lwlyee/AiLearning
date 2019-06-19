#coding=utf-8
import sys
import random
import numpy as np
from matplotlib import pyplot as plt

fname = sys.argv[1]
k = int(sys.argv[2])

x, y = np.loadtxt(fname, delimiter=',', comments='#', unpack=True)#读取数据
distance = [0]*len(x)
minDistance = [0]*len(x)
own = [0]*len(x)
pointX = []
pointY = []
color = ['blue', 'green', 'red', 'yellow', 'black', 'magenta', 'cyan']
plt.xlabel("x")
plt.ylabel("y")

def generatePoint(x,y,k):
    pointX.clear()
    pointY.clear()
    i = random.randint(0, len(x)-1)
    tempx, tempy = x[i], y[i]
    pointX.append(tempx)
    pointY.append(tempy)
    for n in range(k-1):
        for i in range(len(x)):
            distance[i] = sum(findDistance(x[i], y[i], pointX, pointY))
        j = distance.index(max(distance))
        tempx, tempy = x[j], y[j]
        pointX.append(tempx)
        pointY.append(tempy)
    # print(pointX, pointY)
    # plt.scatter(x, y, marker='o')
    # plt.scatter(pointX, pointY, marker='+', c='black', s=100)
    # plt.show()

def findDistance(x, y, pointX, pointY):
    return(list(map(lambda tempx, tempy: ((x - tempx)**2 + (y - tempy)**2)**0.5, pointX, pointY)))

def kmeans(x, y):
    generatePoint(x, y, k)
    times = 0
    while times < 12:
        # plt.scatter(pointX, pointY, marker='+', c='black', s=100)
        for i in range(len(x)):
            distance[i] = findDistance(x[i], y[i], pointX, pointY)
            minDistance[i] = min(distance[i])
            own[i] = distance[i].index(minDistance[i])
        for i in range(k):
            tempx = []
            tempy = []
            for index, value in enumerate(own):
                if value == i:
                    tempx.append(x[index])
                    tempy.append(y[index])
            if len(tempx) == 0:
                kmeans(x,y)
                return
            pointX[i] = sum(tempx)/len(tempx)
            pointY[i] = sum(tempy)/len(tempy)
            plt.scatter(tempx, tempy, marker='o', c=color[i])
        # plt.title('the ' +  str(times+1) + ' time' )
        # plt.scatter(pointX, pointY, marker='x')
        # plt.show()
        times += 1
    plt.scatter(pointX, pointY, marker='x')
    plt.show()

kmeans(x,y)
