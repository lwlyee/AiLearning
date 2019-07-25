#coding=utf-8
import random
import copy
import time

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
    trainDataInfo = []
    tempGroup = []
    for i in range(len(dataType) - 1):
        temp = [0 for i in range(len(dataType[i]))]
        tempGroup.append(temp)
    for unit in dataType[-1]:
        temp = copy.deepcopy(tempGroup)
        temp.append(0)
        trainDataInfo.append(temp)
    for unit in trainData:
        for i in range(len(unit) - 1):
            trainDataInfo[dataType[-1].index(unit[-1])][i][dataType[i].index(unit[i])] += 1
        trainDataInfo[dataType[-1].index(unit[-1])][-1] += 1
    return trainDataInfo

def test(testData, trainDataInfo, dataType, lenData):
    errorNum = 0
    for unit in testData:
        temp = []
        for i in range(len(trainDataInfo)):
            tempNum = 1
            for j in range(len(unit)-1):
                tempNum *= float(trainDataInfo[i][j][dataType[j].index(unit[j])]/trainDataInfo[i][-1])
            tempNum *= float(trainDataInfo[i][-1]/lenData)
            temp.append(tempNum)
        type = dataType[-1][temp.index(max(temp))]
        if unit[-1] != type:
            errorNum += 1
    print('error rate:')
    print("%.2f" % float(errorNum/len(testData)))

if __name__=='__main__':
    start = time.clock()
    trainData, testData, dataType = loadData('adult.data')# adult.data
    trainDataInfo = train(trainData, dataType)
    test(testData, trainDataInfo, dataType, len(trainData))
    end = time.clock()
    print('Running time: %s Seconds' % ("%.2f" % (end - start)))