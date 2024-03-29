#coding=utf-8
import random
import copy

tree = []
stack = []
treeGroup = []

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
    return copy.deepcopy(data[0:int(lenData/2)]), copy.deepcopy(data[int(lenData/2):int(lenData*4/5)]), copy.deepcopy(data[int(lenData*4/5):int(lenData)])

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

def creatTree(popStack):
    data, dataType, dataTypeName, num = popStack[0], popStack[1], popStack[2], popStack[3]
    if countTypeSame(data, dataType):
        drawTree(tree, data[0][-1], 'serise', [len(data)])
        if len(stack) != 0:
            popStack = stack.pop(0)
            creatTree(popStack)
    elif len(dataType) == 1:
        tempCount, tempType = countTypeNum(data, dataType)
        drawTree(tree, tempType, 'serise', tempCount)
        if len(stack) != 0:
            popStack = stack.pop(0)
            creatTree(popStack)
    elif len(data) != 0 and len(dataType) != 1:
        point, pointIndex = findPoint(data, dataType)
        drawTree(tree, point, dataTypeName[pointIndex], num)
        leftTree, rightTree = filter(data, point, pointIndex)
        del dataType[pointIndex]
        del copy.deepcopy(dataTypeName)[pointIndex]
        for unit in data:
            del unit[pointIndex]
        if len(leftTree) != 0 and len(rightTree) != 0:
            pushStack(leftTree[:], dataType[:], dataTypeName[:], [len(leftTree)])
            pushStack(rightTree[:], dataType[:], dataTypeName[:], [len(rightTree)])
        else:
            tree.pop(-1)
            tempTree = leftTree[:] if len(leftTree) != 0 else rightTree[:]
            stack.insert(0, [tempTree, dataType[:], dataTypeName[:], [len(leftTree)]])
        popStack = stack.pop(0)
        creatTree(popStack)
    elif len(data) == 0 and len(stack) != 0:
        popStack = stack.pop(0)
        creatTree(popStack)
    return

def pushStack(data, dataType, dataTypeName, num):
    stack.append([data, dataType, dataTypeName, num])

def drawTree(tree, point ,name, num):
    tree.append([name, point, num])

def countTypeNum(data, dataType):
    count = [0] * len(dataType[-1])
    for unit in data:
        count[dataType[-1].index(unit[-1])] += 1
    return count, dataType[-1][count.index(max(count))]

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
    i = 1
    for unit in tree:
        if unit[0] == 'serise':
            temp = {unit[0]+str(i):unit[1]}
            treeList[0][names[0]].update(temp)
            i += 1
        else:
            temp = {unit[0]+':'+unit[1]:{}}
            treeList[0][names[0]].update(temp)
            names.append(unit[0]+':'+unit[1])
            treeList.append(temp)
        if names[0] == 'root' or len(treeList[0][names[0]]) == 2:
            names.pop(0)
            treeList.pop(0)
    return dictTree

def preparePruning(tree):
    fStack = []
    childPoint = []
    temp = []
    for index, val in enumerate(tree):
        if val[0] != 'serise':
            temp.append(index)
            fStack.append(index)
        elif val[0] == 'serise':
            temp.append(index)
        if len(temp) == 3:
            fStack.pop(0)
            childPoint.append(temp)
            temp = [fStack[0]] if len(fStack) != 0 else []
    leafPoint = copy.deepcopy(childPoint)
    groupPoint = copy.deepcopy(childPoint)
    for i in range(len(leafPoint)-1, -1, -1):
        for j in range(i, -1, -1):
            if leafPoint[i][0] in leafPoint[j] and i != j:
                leafPoint[j].remove(leafPoint[i][0])
                leafPoint[j].extend(leafPoint[i])
                leafPoint[j].remove(leafPoint[i][0])
                leafPoint[j].sort()
    for i in range(len(groupPoint)-1, -1, -1):
        for j in range(i, -1, -1):
            if groupPoint[i][0] in groupPoint[j] and i != j:
                groupPoint[j] = list(set(groupPoint[j]+groupPoint[i]))
    return childPoint, leafPoint, groupPoint

def pruning(tree, childPoint, leafPoint, groupPoint):
    treeGroup.append(tree[:])
    if len(childPoint) == 1:
        return
    tempA = []
    tempFatherPoint = []
    tempSerise = []
    for i in range(len(childPoint)-1, 0, -1):
        A, fatherPoint, serise = getA(tree, childPoint, leafPoint, float(len(tree)), i)
        tempA.append(A)
        tempFatherPoint.append(fatherPoint)
        tempSerise.append(serise)
    delPoint = tempFatherPoint[tempA.index(min(tempA))]
    temp = groupPoint[delPoint][:]
    temp.reverse()
    delLen = tree[temp[-1]][2]
    for unit in temp:
        tree.pop(unit)
    tree.insert(childPoint[delPoint][0], ['serise', tempSerise[tempA.index(min(tempA))], delLen])
    childPoint, leafPoint, groupPoint = preparePruning(tree)
    pruning(tree, childPoint, leafPoint, groupPoint)

def getA(tree, childPoint, leafPoint, totalNum, i):
    child = [sum(tree[childPoint[i][1]][2]), sum(tree[childPoint[i][2]][2])]
    Rt = float(min(child) / totalNum)
    serise = getSerise(tree, childPoint, i)
    leaf = []
    RT = 0
    for index in range(1, len(leafPoint[i])):
        leaf.append(tree[leafPoint[i][index]][2])
    for unit in leaf:
        RT += (sum(unit) - max(unit))/totalNum
    a = "%.2f" % float((Rt - RT)/(len(leafPoint[i])-2))
    return a, i, serise

def getSerise(tree, childPoint, i):
    child = [sum(tree[childPoint[i][1]][2]), sum(tree[childPoint[i][2]][2])]
    index = childPoint[i][child.index(max(child)) + 1]
    temp = tree[index]
    if temp[0] == 'serise':
        serise = temp[1]
    else:
        for j in range(len(childPoint)):
            if childPoint[j][0] == index:
                serise = getSerise(tree, childPoint, j)
    return serise

def testTree(tree, data):
    tempDict = dictTree(tree)['root']
    errorNum = 0
    for unit in data:
        serise = classify(tempDict, unit, 0)
        if serise != unit[-1]:
            errorNum += 1
    errorRate = "%.2f" % float(errorNum/float(len(data)))
    return errorRate


def classify(dictTree, data, i):
    tempstr = list(dictTree.keys())[i]
    while tempstr.find('serise') != -1:
        return list(dictTree.values())[0]
    key, val = tempstr.split(':', 1)
    # print(dataTypeName)
    # print(key)
    # print(data)
    if data[dataTypeName.index(key)] <= val:
        serise = classify(dictTree[tempstr], data, 0)
    else:
        serise = classify(dictTree[tempstr], data, 1)
    return serise

if __name__=='__main__':
    trainData, valData, testData = loadData('iris.txt')
    dataType = pretreatment(trainData)
    creatTree([trainData, dataType, dataTypeName, [len(trainData)]])
    print(testTree(tree, testData))
    print(dictTree(tree))
    childPoint, leafPoint, groupPoint = preparePruning(tree)
    pruning(tree, childPoint, leafPoint, groupPoint)
    errorRate = []
    for i in range(len(treeGroup)):
        errorRate.append(testTree(treeGroup[i], valData))
    finalTree = treeGroup[errorRate.index(min(errorRate))]
    print(testTree(finalTree, testData))
    print(dictTree(finalTree))
