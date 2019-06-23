#coding=utf-8
import sys
import random
from matplotlib import pyplot as plt

pointX = []
pointY = []
color = ['blue', 'green', 'red', 'yellow', 'black', 'magenta', 'cyan']
plt.xlabel("x")
plt.ylabel("y")

def loadData(fname):
    f = open(fname, mode='r', encoding='utf-8')
    next(f)
    line = f.readline()
    x = [];y = []
    while line:
        line = line.replace('\n', '')
        tempStr = line.split(',')
        x.append(float(tempStr[0]));
        y.append(float(tempStr[1]))
        line = f.readline()
    f.close()
    return x, y

def generatePoint(x,y,k):
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

def kmeans(fname, k):
    x, y = loadData(fname)
    global distance; global minDistance; global own
    distance = [0] * len(x)
    minDistance = [0] * len(x)
    own = [0] * len(x)
    generatePoint(x, y, k)
    times = 0
    while times < 12:
        # plt.scatter(pointX, pointY, marker='+', c='black', s=100)#每轮展示
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
            plt.scatter(tempx, tempy, marker='o', c=color[i])
        # plt.title('the ' +  str(times+1) + ' time')#每轮
        # plt.scatter(pointX, pointY, marker='x')#每轮
        # plt.show()#每轮
        times += 1
    plt.scatter(pointX, pointY, marker='x')#一次
    plt.show()#一次

kmeans(sys.argv[1],int(sys.argv[2]))
