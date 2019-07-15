#coding=utf-8
import random
from matplotlib import pyplot as plt

tree = []
stack = []
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
    return data[0:int(lenData)], data[int(lenData/2):int(lenData*4/5)], data[int(lenData*4/5):int(lenData)]

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

def creatTree(data, dataType, dataTypeName):
    if countTypeSame(data, dataType):
        drawTree(tree, data[0][-1], 'serise')
        if len(stack) != 0:
            popStack = stack.pop(0)
            creatTree(popStack[0], popStack[1], popStack[2])
    elif len(dataType) ==1:
        drawTree(tree, countTypeNum(data, dataType), 'serise')
        if len(stack) != 0:
            popStack = stack.pop(0)
            creatTree(popStack[0], popStack[1], popStack[2])
    elif len(data) != 0 and len(dataType) != 1:
        point, pointIndex = findPoint(data, dataType)
        drawTree(tree, point, dataTypeName[pointIndex])
        leftTree, rightTree = filter(data, point, pointIndex)
        del dataType[pointIndex]
        del dataTypeName[pointIndex]
        for unit in data:
            del unit[pointIndex]
        pushStack(leftTree[:], dataType[:], dataTypeName[:])
        pushStack(rightTree[:], dataType[:], dataTypeName[:])
        popStack = stack.pop(0)
        creatTree(popStack[0], popStack[1], popStack[2])
    elif len(data) == 0 and len(stack) != 0:
        popStack = stack.pop(0)
        creatTree(popStack[0], popStack[1], popStack[2])
    return

def pushStack(data, dataType, dataTypeName):
    stack.append([data, dataType, dataTypeName])

def drawTree(tree, point ,name):
    tree.append([name, point])
    print(tree)

def countTypeNum(data, dataType):
    count = [0] * len(dataType[-1])
    for unit in data:
        count[dataType[-1].index(unit[-1])] += 1
    return dataType[-1][count.index(max(count))]

def countTypeSame(data, dataType):
    count = [0] * len(dataType[-1])
    for unit in data:
        if count[dataType[-1].index(unit[-1])] ==0:
            count[dataType[-1].index(unit[-1])] += 1
    # print(sum(count) == 1)
    return sum(count) == 1

def filter(data, point, pointIndex):
    leftTree = []
    rightTree = []
    Flag = 0 if type(eval(point)) == str else 1
    for i in range(len(data)):
        if (data[i][pointIndex] < point) and Flag:
            leftTree.append(data[i])
        elif (data[i][pointIndex] == point) and (not Flag):
            leftTree.append(data[i])
        else:
            rightTree.append(data[i])
    # print(len(leftTree))
    # print(len(rightTree))
    return leftTree, rightTree

def findPoint(data, dataType):
    Gini = []
    select = []
    for i in range(len(dataType)-1):
        if dataType[i] == 'num':
            tempGini, tempSelect = getContinueGini(data, i, dataType)
        else:
            print("not ok")
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


def dictTree(tree):
    dictTree = {'root':{}}
    treeList = [dictTree]
    names = ['root']
    for unit in tree:
        if unit[0] == 'serise':
            temp = {unit[0]:unit[1]}
            treeList[0][names[0]].update(temp)
        else:
            temp = {unit[0]+':'+unit[1]:{}}
            treeList[0][names[0]].update(temp)
            names.append(unit[0]+':'+unit[1])
            treeList.append(temp)
        if names[0] == 'root' or len(treeList[0][names[0]]) == 2:
            names.pop(0)
            treeList.pop(0)
    print(dictTree)


if __name__=='__main__':
    trainData, valData, testData = loadData('iris.txt')
    dataType = pretreatment(trainData)
    creatTree(trainData, dataType, dataTypeName)
    dictTree(tree)