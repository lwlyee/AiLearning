#coding=utf-8
import random
import copy

def loadData(fname):
    data = []
    dataType = []
    f = open(fname, mode='r', encoding='utf-8')
    line = f.readline()
    tempStr = line.split(',')
    for i in range(len(tempStr)):
        dataType.append(set())
    while line:
        line = line.replace('\n', '')
        tempStr = line.split(',')
        for i in range(len(dataType)):
            dataType[i].add(tempStr[i])
        data.append(tempStr)
        line = f.readline()
    f.close()
    for i in range(len(dataType)):
        dataType[i] = list(dataType[i])
        dataType[i].sort()
    random.shuffle(data)
    lenData = len(data)
    return data[:int(lenData/2)], data[int(lenData/2):], dataType

def train(trainData, dataType):
    trainDataInfo, pList = getDataInfo(trainData, dataType)
    pList = getP(trainDataInfo, pList, len(trainData))
    return pList

def getDataInfo(trainData, dataType):
    trainDataInfo = []
    tempGroup = []
    pList = []
    for i in range(len(dataType)-1):
        temp = [0 for i in range(len(dataType[i]))]
        tempGroup.append(temp)
    for unit in dataType[-1]:
        temp = copy.deepcopy(tempGroup)
        temp.append(0)
        trainDataInfo.append(temp)
        pList = copy.deepcopy(trainDataInfo)
    for unit in trainData:
        for i in range(len(unit)-1):
            trainDataInfo[dataType[-1].index(unit[-1])][i][dataType[i].index(unit[i])] += 1
        trainDataInfo[dataType[-1].index(unit[-1])][-1] += 1
    return trainDataInfo, pList

def getP(trainDataInfo, pList, lenData):
    for i in range(len(trainDataInfo)):
        pList[i][-1] = "%.4f" % float(trainDataInfo[i][-1]/lenData)
        for j in range(len(trainDataInfo[i])-1):
            for k in range(len(trainDataInfo[i][j])):
                pList[i][j][k] = "%.4f" % float(trainDataInfo[i][j][k]/sum(trainDataInfo[i][j]))
    return pList

def test(testData, pList, dataType):
    errorNum = 0
    for unit in testData:
        temp = []
        for i in range(len(pList)):
            tempNum = 1
            for j in range(len(unit)-1):
                tempNum *= float(pList[i][j][dataType[j].index(unit[j])])
            tempNum *= float(pList[i][-1])
            temp.append(tempNum)
        type = dataType[-1][temp.index(max(temp))]
        if unit[-1] != type:
            errorNum += 1
    print('error rate:')
    print("%.2f" % float(errorNum/len(testData)))

if __name__=='__main__':
    trainData, testData, dataType = loadData('car.data')
    pList = train(trainData, dataType)
    test(testData, pList, dataType)