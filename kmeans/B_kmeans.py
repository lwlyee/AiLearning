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
#上述代码的详细注释，请转kmeans.py
def B_kmeans(fname, k):
    B_x = []
    B_y = []
    B_pointx = []
    B_pointy = []
    SSE = []
    listx, listy = loadData(fname)
    for i in range(k-1):#在未找到k个质点之前，重复执行
        tempPointx, tempPointy, temp_x, temp_y, tempSSE = getSSE(listx, listy)
        B_pointx.extend(tempPointx);B_pointy.extend(tempPointy)#保存一次二分后的质点组
        B_x.extend(temp_x);B_y.extend(temp_y)#保存一次二分后每个簇中的数据点
        SSE.extend(tempSSE)#保存当前各簇的SSE
        maxSSE = 0
        whichCluster = 0
        for n in range(len(B_x)):#找到当前各簇中SSE最大的簇
            tempSSE = SSE[n]
            if tempSSE > maxSSE:
                maxSSE = tempSSE
                whichCluster = n
        listx = B_x[whichCluster];listy = B_y[whichCluster]#以SSE最大的簇在下一轮继续进行二分
        if i != k - 2:#除了进行最后一次二分簇，均将当前SSE最大的簇继续进行二分，并需要删除该簇所记录的各种信息.
            del B_x[whichCluster];del B_y[whichCluster]
            del B_pointx[whichCluster];del B_pointy[whichCluster]
            del SSE[whichCluster]
    draw(B_x, B_y, B_pointx, B_pointy)#根据最后记录的k个簇的信息进行绘图

def getSSE(listx, listy):#对于输入的数据点，做二分kmeans。并返回二分后每个簇的质点，每个簇所包含的数据点，以及总的SSE
    SSEx = [[], []];SSEy = [[], []]
    tempPointX, tempPointY = kmeans(listx, listy, 2)
    for index, value in enumerate(own):
        SSEx[value].append(listx[index])
        SSEy[value].append(listy[index])
    SSE = countSSE(tempPointX, tempPointY, SSEx, SSEy)
    return tempPointX, tempPointY, SSEx, SSEy, SSE

def countSSE(tempPointX, tempPointY, SSEx, SSEy):#根据簇的质点以及簇中所包含的数据点，计算该簇的SSE
    temp = []
    for i in range(2):
        list = findDistance(tempPointX[i], tempPointY[i], SSEx[i], SSEy[i])
        temp.append(sum(map(lambda x: x ** 2, list)))
    return temp

def draw(B_x, B_y, B_pointx, B_pointy):#根据数据点和质点绘图
    for i in range(len(B_x)):
        plt.scatter(B_x[i], B_y[i], marker='o', c=color[i])
    plt.scatter(B_pointx, B_pointy, marker='x')
    plt.show()

B_kmeans(sys.argv[1], int(sys.argv[2]))
