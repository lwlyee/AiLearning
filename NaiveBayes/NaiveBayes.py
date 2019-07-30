#coding=utf-8
import random
import copy
import time

def loadData(fname):
    '''载入数据随机分为训练集和测试集，并将每个特征所拥有的属性值记录在dataType中'''
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
    '''
    通过训练集得到各个分类的各个特征属性所占有的样本数
    存储的数据格式如下：（设有三个分类，4个特征，特征属性各位分别为3，3，2，4.设训练集共有100个样本）
    [[[5,7,13],[14,8,3],[12,13],[5,5,3,12],25],
    [[14,30,20],[25,25,4],[26,28],[13,21,15,5],54],
    [[4,7,10],[8,6,7],[12,9],[4,5,4,8],21]]
    '''
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
    '''
    根据train()所得的数据，对测试集中每一个数据计算P(yi)和P(xi|yi)
    再根据朴素贝叶斯的原理选取概率最大的类别作为分类结果
    以上述数据格式为例，设某测试数据特征值对应位置分别为0，0，1，3
    则该测试数据属于第一类的概率P=(5/25)*(14/25)*(12/25)*(3/25)*(25/100)
    以此类推求第二类，第三类概率
    '''
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
    '''
    算法原理：1.根据训练集求出每类的P(yi),以及该类下各个特征属性的概率P(xi|yi)
    2.根据测试集计算数据属于某类的概率P(yi|X)=(P(xi|yi)*......*P(xj|yi)*P(yi))/P(X)，P(X)因为对每个数据是相同的可以省去
    '''
    start = time.clock()
    trainData, testData, dataType = loadData('adult.data')# adult.data
    trainDataInfo = train(trainData, dataType)
    test(testData, trainDataInfo, dataType, len(trainData))
    end = time.clock()
    print('Running time: %s Seconds' % ("%.2f" % (end - start)))
