#coding=utf-8
import sys
import random
from matplotlib import pyplot as plt

pointX = []#质点组
pointY = []
color = ['blue', 'green', 'red', 'yellow', 'black', 'magenta', 'cyan']
plt.xlabel("x")
plt.ylabel("y")

def loadData(fname):
    '''加载数据，并返回读取的所有数据点的x，y值,分别存在两个列表中'''
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
    return x, y#

def generatePoint(x,y,k):
    '''找到k个初始点：先随机数据点中的一个作为第一个初始点，再在剩余点中找到与之距离最远的点作为第二个初始点，以此类推找到k个初始点'''
    i = random.randint(0, len(x)-1)
    tempx, tempy = x[i], y[i]
    pointX.append(tempx)
    pointY.append(tempy)
    for n in range(k-1):
        tempx, tempy = findFarPoint(x, y)
        pointX.append(tempx)
        pointY.append(tempy)

def findFarPoint(x, y):
    '''计算数据中所有点与当前质点组距离和，并返回距离最大的点的坐标'''
    for i in range(len(x)):
        distance[i] = sum(findDistance(x[i], y[i], pointX, pointY))
    j = distance.index(max(distance))
    return x[j], y[j]

def findDistance(x, y, pointX, pointY):
    '''计算传入的点（x,y）与当前质点组中各个质点的距离，并一并存入一个列表中返回'''
    return(list(map(lambda tempx, tempy: ((x - tempx)**2 + (y - tempy)**2)**0.5, pointX, pointY)))

def kmeans(fname, k):
    '''
    算法原理：1.先找到k个初始质点。2.对每个数据点，都计算与当前每个质点的距离，找到距离最近的质点，并将该数据点归属到该质点所在的簇。
    3.根据每簇所包含的数据点更新该簇的质点。4.达到终止条件，分类完毕。
    '''
    x, y = loadData(fname)
    global distance; global minDistance; global own
    distance = [0] * len(x)
    minDistance = [0] * len(x)
    own = [0] * len(x)#用来保存每个数据所在的归属簇标号
    generatePoint(x, y, k)#生成k个质点，并将其坐标保存在全局变量质点组中
    times = 0
    while times < 12:
        # plt.scatter(pointX, pointY, marker='+', c='black', s=100)#每轮 每轮画图，可看出本轮质点和上轮质点之间的偏移
        for i in range(len(x)):#
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
            if len(tempx) == 0:#对于某个质点出现空簇的情况，则抛弃该质点，重新选出一个质点
                pointX[i], pointY[i] = findFarPoint(x, y)
            else:
                pointX[i] = sum(tempx)/len(tempx)
                pointY[i] = sum(tempy)/len(tempy)
            plt.scatter(tempx, tempy, marker='o', c=color[i])
        # plt.title('the ' +  str(times+1) + ' time')#每轮
        # plt.scatter(pointX, pointY, marker='x')#每轮
        # plt.show()#每轮
        times += 1
    plt.scatter(pointX, pointY, marker='x')#一次画图，只画出最后分簇后的质点
    plt.show()#一次

if __name__=='__main__':
    kmeans(sys.argv[1],int(sys.argv[2]))
