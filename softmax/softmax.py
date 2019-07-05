#coding=utf-8
import sys
import numpy as np
from matplotlib import pyplot as plt

color = ['blue', 'green', 'red', 'yellow', 'black', 'magenta', 'cyan']
plt.xlabel("x")
plt.ylabel("y")

def loadData(fname, fileType):
    valueMat = [];typeMat = [];valueMatSet = set()
    f = open(fname, mode='r', encoding='utf-8')
    next(f)
    line = f.readline()
    while line:
        line = line.replace('\n', '')
        tempStr = line.split(',')
        valueMat.append([1.0, float(tempStr[0]), float(tempStr[1])])
        if fileType == 1:
            typeMat.append(int(tempStr[2]))
            plt.scatter(float(tempStr[0]), float(tempStr[1]), color=color[int(tempStr[2])])
        line = f.readline()
    for i in range(len(typeMat)):  # 对所有数据的类别进行整理，整理出实际的数据分类种类
        valueMatSet.add(typeMat[i])
        typeNum = len(list(valueMatSet))
    f.close()
    valueMat = np.mat(valueMat)
    typeMat = np.mat(typeMat).transpose()
    return valueMat, typeMat, typeNum

def softmax(num):
    tempExp = np.exp(num)
    tempSum = np.exp(num).sum(axis=1)
    return np.divide(tempExp, tempSum)

if __name__ == '__main__':
    trainValueMat, trainTypeMat, typeNum = loadData('train.txt', 1)
    errorMat = np.zeros([len(trainValueMat), typeNum],dtype=float)
    for i in range(len(trainTypeMat)):
        tempMat = [0]*typeNum
        tempMat[int(trainTypeMat[i]-1)] = -1
        errorMat[i] = tempMat
    m, n = np.shape(trainValueMat)
    stepSize = 0.001
    times = 10000
    weights = np.ones((n, typeNum))
    for i in range(times):
        prediction = softmax(trainValueMat*weights)
        error = prediction + errorMat
        weights = weights - stepSize * trainValueMat.transpose() * error
        predictiont = softmax(trainValueMat*weights)
        predictiont = list(predictiont)
        errorNum = 0
        for j in range(len(predictiont)):
            temp = predictiont[j].tolist()
            k = temp[0].index(max(temp[0]))+1
            if k != int(trainTypeMat[j].tolist()[0][0]):
                errorNum += 1
        if i % 100 == 0:
            print('第' + str(i+100) + '次迭代 正确率：' + str(float((len(predictiont) - errorNum)/len(predictiont))))