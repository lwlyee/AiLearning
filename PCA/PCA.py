#coding=utf-8
import numpy as np
import copy

def loadData(fname):
    f = open(fname, mode='r', encoding='utf-8')
    data = []
    line = f.readline()
    while line:
        line = line.replace('\n', '')
        tempStr = line.split(',')
        tempStr.pop(0)
        tempStr = list(map(float, tempStr))
        data.append(tempStr)
        line = f.readline()
    f.close()
    return np.mat(data).T

def pretreatmentData(data):
    '''对数据归一化和中心化'''
    max = data.max(axis=1)
    min = data.min(axis=1)
    data = (data - min)/(max - min)
    mean = np.mean(data, axis=1)
    return data - mean

def getCovariance(data):
    '''返回特征值，特征向量和协方差矩阵'''
    n, m = data.shape
    Covariance = (1/m)*(data*data.T)
    eigenvalue, eigenvector = np.linalg.eig(Covariance)
    return eigenvalue, eigenvector, Covariance

def getK(Covariance):
    '''确定合适的降维维数k'''
    m, n = Covariance.shape
    sum = 0
    covarianceList = []
    for i in range(m):
        sum += Covariance[i, i]
        covarianceList.append(Covariance[i, i])
    print(covarianceList)
    covarianceList.sort(reverse=True)
    temp = 0
    for i in range(m):
        temp += covarianceList[i]
        if temp/sum >= 0.90:
            return i+1

def getBase(eigenvalue, eigenvector, k):
    '''得到降维所需要的基底'''
    eigenvalue = list(eigenvalue)
    temp = copy.deepcopy(eigenvalue)
    eigenvalue.sort(reverse=True)
    tempeigenvalue = eigenvalue[:k]
    base = eigenvector[:, 0]
    for i in range(1, len(tempeigenvalue)):
        base = np.hstack((base, eigenvector[:, temp.index(eigenvalue[i])]))
    return base.T

if __name__=="__main__":
    '''
    算法思路：
    1.加载数据并归一化中心化处理。2.通过数据计算协方差矩阵并计算该矩阵的特征值和特征向量。
    3.确定维数k。4.取最大的k个特征值对应的特征向量作为基底。5.用基底变换原数据
    '''
    data = loadData("wine.data")
    tempdata = pretreatmentData(data)
    eigenvalue, eigenvector, Covariance = getCovariance(tempdata)
    k = getK(Covariance)
    base = getBase(eigenvalue, eigenvector, k)
    output = base * data
    print("原数据维度：")
    print(data.shape)
    print("降维后数据维度：")
    print(output.shape)


    # 测试验证代码，二维数据降维到一维，结果可视化

    # test = [[0.7166531676453336, 0.6974297364637598], [-0.6974297364637598, 0.7166531676453336]]
    # print(test)
    # test = np.mat(test)
    # print(test * Covariance * test.T)

    # from matplotlib import pyplot as plt
    # color = ['blue', 'green', 'red', 'yellow', 'black', 'magenta', 'cyan']
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.axis('equal')
    # plt.xlim(-0.5, 1.5)
    # plt.ylim(-0.5, 1.5)
    # def draw(x):
    #     y = (base.tolist()[0][1]/base.tolist()[0][0])* x
    #     return y
    # plt.scatter(data.tolist()[0], data.tolist()[1], marker='x', color=color[0])
    # plt.plot([-0.5, 1.5], [draw(-0.5), draw(1.5)], color=color[1])
    # onlinePlot = base.T * output
    # plt.scatter(onlinePlot.tolist()[0], onlinePlot.tolist()[1], marker='x', color=color[2])
    # for i in range(len(data.tolist()[0])):
    #     plt.plot([data.tolist()[0][i], onlinePlot.tolist()[0][i]], [data.tolist()[1][i], onlinePlot.tolist()[1][i]], color=color[6], linestyle='--')
    # plt.show()
