#coding=utf-8
import numpy as np

def loadData(fname):
    f = open(fname, mode='r', encoding='utf-8')
    data = []
    line = f.readline()
    while line:
        line = line.replace('\n', '')
        tempStr = line.split(',')
        tempStr.pop(0)
        data.append(tempStr)
        line = f.readline()
    f.close()
    return np.mat(data).T

def pretreatment(data):
    mean = np.mean(data, axis=0)
    print(mean)
    pass

if __name__=="__main__":
    data = loadData("wine.data")
    pretreatment(data)
    print(data.shape)