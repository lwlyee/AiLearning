#coding=utf-8
import random
from matplotlib import pyplot as plt

def loadData(fname):
    f = open(fname, mode='r', encoding='utf-8')
    next(f)
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
    tree = {}
    findPoint(data, dataType)

def findPoint(data, dataType):
    for i in range(len(dataType)-1):
        if dataType[i] == 'num':
            getContinueGini(data, i, dataType)
        else:
            getDiscreteGini(data, i, dataType)

def getContinueGini(data, i, dataType):
    index = 0
    Gini = []
    tempData = sorted(data, key=lambda x: x[i], reverse=False)
    lenData = float(len(tempData))
    while index != len(tempData) - 1:
        meanNum = (float(tempData[index][i]) + float(tempData[index + 1][i]))/2
        index += 1
        tempCountSmall = [0] * len(dataType[-1])
        tempCountMax = [0] * len(dataType[-1])
        for j in range(len(tempData)):
            if float(tempData[j][i]) <= meanNum:
                tempCountSmall[dataType[-1].index(tempData[j][-1])] += 1
            else:
                tempCountMax[dataType[-1].index(tempData[j][-1])] += 1
        smallGini = 1
        maxGini = 1
        for k in range(len(dataType[-1])):
            sum_tempCountSmall = sum(tempCountSmall) if sum(tempCountMax) != 0 else sum(tempCountSmall)-1
            sum_tempCountMax = sum(tempCountMax) if sum(tempCountMax) != 0 else 1
            smallGini -= (float(tempCountSmall[k])/sum_tempCountSmall)**2
            maxGini -= (float(tempCountMax[k])/sum_tempCountMax)**2
        Gini.append(smallGini*(sum(tempCountSmall)/lenData) + maxGini*(sum(tempCountMax)/lenData))
    print(Gini)
    print(Gini.index(min(Gini)))
    print(min(Gini))
    return min(Gini)

def getDiscreteGini(data, dataType):
    pass

if __name__=='__main__':
    trainData, valData, testData = loadData('iris.txt')
    dataType = pretreatment(trainData)
    creatTree(trainData, dataType)