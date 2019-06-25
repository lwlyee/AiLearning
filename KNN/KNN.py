#coding=utf-8
import sys
from matplotlib import pyplot as plt

color = ['blue', 'green', 'red', 'yellow', 'black', 'magenta', 'cyan']
plt.xlabel("x")
plt.ylabel("y")
FLAG = 0

def loadData(fname, type):
    f = open(fname, mode='r', encoding='utf-8')
    if type == 'p':
        next(f)
    line = f.readline()
    x = [];y = [];p_type = []
    while line:
        line = line.replace('\n', '')
        tempStr = line.split(',')
        x.append(float(tempStr[0]));y.append(float(tempStr[1]))
        if type == 'p':
            p_type.append(tempStr[2])
        line = f.readline()
    f.close()
    if type == 'p':
        return x, y, p_type
    return x, y

def findDistance(x, y, pointX, pointY):
    return(list(map(lambda tempx, tempy: ((x - tempx)**2 + (y - tempy)**2)**0.5, pointX, pointY)))

def countMax(list, p_typeValue):
    temp = 0
    for i in range(len(p_typeValue)):
        if list.count(p_typeValue[i]) > temp:
            temp = list.count(p_typeValue[i])
            value = p_typeValue[i]
    return value

def countWeightMax(list, p_typeValue, tempDistance):
    temp = [0]*3
    for i in range(len(list)):
        temp[p_typeValue.index(list[i])] += 1/tempDistance[i]
    value = p_typeValue[temp.index(max(temp))]
    return value

def crossVerify(x, y, type):
    tempP = [[[], [], []]]*10
    tempT = [[[], [], []]]*10
    minRate = 1
    minK = 0
    num = int(len(x)/10) if len(x)%10 == 0 else int(len(x)/10 + 1)
    lack = num*10 - len(x)
    for i in range(10):
        if i == 0:
            numStart = 0
        elif i < lack:
            numStart = numEnd -1
        else:
            numStart = numEnd
        numEnd = numStart + num
        tempT[i][0], tempT[i][1], tempT[i][2] = x[numStart:numEnd], y[numStart:numEnd], type[numStart:numEnd]
        tempP[i][0], tempP[i][1], tempP[i][2] = x[0:numStart] + x[numEnd:len(x)], y[0:numStart] + y[numEnd:len(x)], type[0:numStart] + type[numEnd:len(x)]
    for k in range(2,20):
        errorNum = 0
        errorRate = []
        for i in range(10):
            tempType = KNN(tempP[i], tempT[i], k)
            for j in range(num):
                if tempT[i][2][j] != tempType[j]:
                    errorNum += 1
            errorRate.append(float(errorNum)/float(num))
        if sum(errorRate)/10 <= minRate:
            minK = k
    global FLAG
    FLAG = 1
    return minK


def KNN(pFile, tFile, k):
    t_type = []
    p_typeSet = set()
    if k == '':
        p_x, p_y, p_type = loadData(pFile, 'p')
        t_x, t_y = loadData(tFile, 't')
        k = crossVerify(p_x, p_y, p_type)
    else:
        p_x, p_y, p_type = pFile[0], pFile[1], pFile[2]
        t_x, t_y = tFile[0], tFile[1]
    for i in range(len(p_type)):
        p_typeSet.add(p_type[i])
        p_typeValue = list(p_typeSet)
    f = open('result.txt', mode='w', encoding='utf-8')
    for i in range(len(t_x)):
        distance = findDistance(t_x[i], t_y[i], p_x, p_y)
        tempDistance = distance[:]
        tempDistance.sort(reverse=False)
        tempDistance = tempDistance[0:k]
        type = []
        for j in range(len(tempDistance)):
            type.append(p_type[distance.index(tempDistance[j])])
        # t_type.append(countMax(type, p_typeValue))#普通地计算点的个数
        if tempDistance[0] == 0:
            t_type.append(p_type[distance.index(0)])
        else:
            t_type.append(countWeightMax(type, p_typeValue, tempDistance))#对距离进行加权计算
    if FLAG == 0:
        return t_type
    else:
        for i in range(len(t_x)):
            plt.scatter(t_x[i], t_y[i], marker='x', color=color[p_typeValue.index(t_type[i])], s=100)
            f.write(str(t_x[i]) + ',' + str(t_y[i]) + ',' + str(t_type[i]) + '\n')
        for i in range(len(p_x)):
            plt.scatter(p_x[i], p_y[i], marker='o', color=color[p_typeValue.index(p_type[i])])
        plt.show()

KNN(sys.argv[1], sys.argv[2], '')