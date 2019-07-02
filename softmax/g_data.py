#coding=utf-8
import sys
import random
#以kmeans中的算法为基础，稍加改动，生成n个随机不重复的数据点，并用kmeans算法为其分类，标记后存入文件
x = []
y = []
pointX = []
pointY = []
group = set()
laber = [1, 2, 3, 4, 5, 6, 7]
randomfloat = lambda arg1, arg2: float('%.03f'%random.uniform(int(arg1), int(arg2)))

f = open('data.txt', mode='w+', encoding='utf-8')
temp = '#' + '随机生成x范围为' + sys.argv[1] + "-" + sys.argv[2] + ",y范围为" + sys.argv[3] + "-" + sys.argv[4] + "的不重复数据点" + sys.argv[5] + "个，并分成" + sys.argv[6] + '簇\n'
f.write(str(temp))
f.close()

setlen = len(group)
while len(group) < int(sys.argv[5]):
    tempx = randomfloat(sys.argv[1], sys.argv[2])
    tempy = randomfloat(sys.argv[3], sys.argv[4])
    group.add((tempx, tempy))
    if setlen != len(group):
        x.append(tempx)
        y.append(tempy)

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

def kmeans(x, y, k):
    global distance; global minDistance; global own
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
    f = open('data.txt', mode='a', encoding='utf-8')
    for i in range(len(x)):
        f.write(str(x[i]) + ',' + str(y[i]) + ',' + str(laber[int(own[i])]) + '\n')
    f.close()

kmeans(x, y, int(sys.argv[6]))
