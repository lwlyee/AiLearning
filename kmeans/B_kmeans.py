#coding=utf-8
import sys
import random
import numpy as np
from matplotlib import pyplot as plt

pointX = []
pointY = []
color = ['blue', 'green', 'red', 'yellow', 'black', 'magenta', 'cyan']
plt.xlabel("x")
plt.ylabel("y")

def loadData(fname):
    x, y = np.loadtxt(fname, delimiter=',', comments='#', unpack=True)  # 读取数据
    return x, y

def generatePoint(x,y,k):
    pointX.clear()
    pointY.clear()
    i = random.randint(0, len(x)-1)
    tempx, tempy = x[i], y[i]
    pointX.append(tempx)
    pointY.append(tempy)
    for n in range(k-1):
        tempx, tempy = findFarPoint(x, y)
        pointX.append(tempx)
        pointY.append(tempy)

def findFarPoint(x, y):
    for i in range(len(x)):
        distance[i] = sum(findDistance(x[i], y[i], pointX, pointY))
    j = distance.index(max(distance))
    return x[j], y[j]

def findDistance(x, y, pointX, pointY):
    return(list(map(lambda tempx, tempy: ((x - tempx)**2 + (y - tempy)**2)**0.5, pointX, pointY)))

def kmeans(x, y, k):
    global distance;global minDistance;global own
    distance = [0] * len(x)
    minDistance = [0] * len(x)
    own = [0] * len(x)
    generatePoint(x, y, k)
    times = 0
    while times < 12:
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
                pointX[i], pointY[i] = findFarPoint(x, y)
            else:
                pointX[i] = sum(tempx)/len(tempx)
                pointY[i] = sum(tempy)/len(tempy)
        times += 1
        return pointX, pointY
#上述部分相比于kmeans.py，只对读取数据部分以及kmeans函数运行结果的返回进行了修改

def B_kmeans(fname, k):
    B_x = []
    B_y = []
    B_pointx = []
    B_pointy = []
    SSE = []
    listx, listy = loadData(fname)
    for i in range(k-1):
        tempPointx, tempPointy, temp_x, temp_y, tempSSE = getSSE(listx, listy)
        B_pointx.extend(tempPointx);B_pointy.extend(tempPointy)
        B_x.extend(temp_x);B_y.extend(temp_y)
        SSE.extend(tempSSE)
        maxSSE = 0
        whichCluster = 0
        for n in range(len(B_x)):
            tempSSE = SSE[n]
            if tempSSE > maxSSE:
                maxSSE = tempSSE
                whichCluster = n
        listx = B_x[whichCluster];listy = B_y[whichCluster]
        if i != k - 2:
            del B_x[whichCluster];del B_y[whichCluster]
            del B_pointx[whichCluster];del B_pointy[whichCluster]
            del SSE[whichCluster]
    draw(B_x, B_y, B_pointx, B_pointy)


def getSSE(listx, listy):
    SSEx = [[], []];SSEy = [[], []]
    tempPointX, tempPointY = kmeans(listx, listy, 2)
    for index, value in enumerate(own):
        SSEx[value].append(listx[index])
        SSEy[value].append(listy[index])
    SSE = countSSE(tempPointX, tempPointY, SSEx, SSEy)
    return tempPointX, tempPointY, SSEx, SSEy, SSE

def countSSE(tempPointX, tempPointY, SSEx, SSEy):
    temp = []
    for i in range(2):
        list = findDistance(tempPointX[i], tempPointY[i], SSEx[i], SSEy[i])
        temp.append(sum(map(lambda x: x ** 2, list)))
    return temp

def draw(B_x, B_y, B_pointx, B_pointy):
    for i in range(len(B_x)):
        plt.scatter(B_x[i], B_y[i], marker='o', c=color[i])
    plt.scatter(B_pointx, B_pointy, marker='x')
    plt.show()

B_kmeans(sys.argv[1], int(sys.argv[2]))