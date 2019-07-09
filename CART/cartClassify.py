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
    tempCountSmall = [0]*len(tempData[-1])
    tempCountMax = [0]*len(tempData[-1])
    Gini = [0]*len(tempData[-1])
    tempData = sorted(data, key=lambda x: x[i], reverse=False)
    while index != len(tempData) - 2:
        meanNum = (float(tempData[index][i]) + float(tempData[index + 1][i]))/2
        index += 1
        for j in range(len(tempData)):
            if tempData[j][i] <= meanNum:
                tempCountSmall[dataType[-1].index(tempData[j][-1])] += 1
            else:
                tempCountMax[dataType[-1].index(tempData[j][-1])] += 1
        for k in range(len(dataType)):
            Gini[k] = (1 - (tempCountSmall[k]/len(tempData))**2)* +(1 - (tempCountMax[k]/len(tempData))**2)*


def getDiscreteGini(data, dataType):
    pass

if __name__=='__main__':
    trainData, valData, testData = loadData('iris.txt')
    dataType = pretreatment(trainData)
    creatTree(trainData, dataType)