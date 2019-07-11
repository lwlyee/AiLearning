#coding=utf-8
import random
from matplotlib import pyplot as plt

tree = []

def loadData(fname):
    f = open(fname, mode='r', encoding='utf-8')
    line = f.readline()
    line = line.replace('\n', '')
    tempStr = line.split(' ')
    global dataTypeName
    dataTypeName = [tempStr[0], tempStr[1], tempStr[2], tempStr[3], tempStr[4]]
    line = f.readline()
    data = []
    while line:
        line = line.replace('\n', '')
        tempStr = line.split(' ')
        tempData = [tempStr[1], tempStr[2], tempStr[3], tempStr[4], tempStr[5]]
        data.append(tempData)
        line = f.readline()
    f.close()
    random.shuffle(data)
    lenData = len(data)
    return data[0:int(lenData/2)], data[int(lenData/2):int(lenData*4/5)], data[int(lenData*4/5):int(lenData)]

def pretreatment(data):
    dataType = []
    for i in range(len(data[0])):
        if (type(eval(trainData[0][i])) == float) | (type(eval(trainData[0][i])) == int):
            dataType.append('num')
        else:
            dataType.append(countNum(data, i))
    return dataType

def countNum(data, j):
    valueType = set()
    for i in range(len(data)):
        valueType.add(data[i][j])
    return list(valueType)

def creatTree(data, dataType):
    if endJudge(data, dataType):
        return
    point, pointIndex = findPoint(data, dataType)
    drawTree(tree, point, pointIndex)
    del dataType[pointIndex]
    del dataTypeName[pointIndex]
    for unit in data:
        del unit[pointIndex]
    leftTree, rightTree = filter(data, point, pointIndex)
    print('2')
    creatTree(leftTree, dataType)
    print('1')
    creatTree(rightTree, dataType)
    return

def drawTree(tree, point ,ponitIndex):
    tree.append({dataTypeName[ponitIndex]: point})
    print(tree)

def endJudge(data, dataType):
    if len(dataType) == 1:
        return 1
    else:
        return 0

def filter(data, point, pointIndex):
    leftTree = []
    rightTree = []
    Flag = 0 if type(eval(point)) == str else 1
    for i in range(len(data)):
        if (data[i][pointIndex] <= point) & Flag:
            leftTree.append(data[i])
        elif (data[i][pointIndex] == point) & (not Flag):
            leftTree.append(data[i])
        else:
            rightTree.append(data[i])
    return leftTree, rightTree

def findPoint(data, dataType):
    Gini = []
    select = []
    for i in range(len(dataType)-1):
        if dataType[i] == 'num':
            tempGini, tempSelect = getContinueGini(data, i, dataType)
        else:
            tempGini, tempSelect = getDiscreteGini(data, i, dataType)
        Gini.append(tempGini)
        select.append(tempSelect)
    return select[Gini.index(min(Gini))], Gini.index(min(Gini))

def getContinueGini(data, i, dataType):
    Gini = []
    meanNum = []
    tempData = sorted(data, key=lambda x: x[i], reverse=False)
    for index in range(len(tempData) - 1):
        meanNum.append((float(tempData[index][i]) + float(tempData[index + 1][i]))/2)
        tempCountSmall = [0] * len(dataType[-1])
        tempCountMax = [0] * len(dataType[-1])
        for j in range(len(tempData)):
            if float(tempData[j][i]) <= meanNum[index]:
                tempCountSmall[dataType[-1].index(tempData[j][-1])] += 1
            else:
                tempCountMax[dataType[-1].index(tempData[j][-1])] += 1
        Gini.append(getGini(data, tempCountSmall, tempCountMax, dataType))
    return min(Gini), "%.2f" % meanNum[Gini.index(min(Gini))]

def getDiscreteGini(data, i, dataType):
    Gini = []
    for index in range(len(dataType[i])):
        tempCountYes = [0] * len(dataType[-1])
        tempCountNo = [0] * len(dataType[-1])
        for j in range(len(data)):
            if data[j][i] == dataType[i][index]:
                tempCountYes[dataType[-1].index(data[j][-1])] += 1
            else:
                tempCountNo[dataType[-1].index(data[j][-1])] += 1
        Gini.append(getGini(data, tempCountYes, tempCountNo, dataType))
    return min(Gini), dataType[i][Gini.index(min(Gini))]

def getGini(data, countA, countB, dataType):
    GiniA = 1
    GiniB = 1
    lenData = float(len(data))
    for k in range(len(dataType[-1])):
        sumCountA = sum(countA) if sum(countB) != 0 else sum(countA) - 1
        sumCountB = sum(countB) if sum(countB) != 0 else 1
        GiniA -= ((float(countA[k]) / sumCountA)) ** 2
        GiniB -= ((float(countB[k]) / sumCountB)) ** 2
    return GiniA * (sumCountA / lenData) + GiniB * (sumCountB / lenData)


if __name__=='__main__':
    trainData, valData, testData = loadData('iris.txt')
    dataType = pretreatment(trainData)
    creatTree(trainData, dataType)