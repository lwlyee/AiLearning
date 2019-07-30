#coding=utf-8
import sys
from matplotlib import pyplot as plt

color = ['blue', 'green', 'red', 'yellow', 'black', 'magenta', 'cyan']
plt.xlabel("x")
plt.ylabel("y")
FLAG = 0

def loadData(fname, type):#加载数据
    f = open(fname, mode='r', encoding='utf-8')
    if type == 'p':
        next(f)
    line = f.readline()
    x = [];y = [];p_type = []
    while line:
        line = line.replace('\n', '')
        tempStr = line.split(',')
        x.append(float(tempStr[0]));y.append(float(tempStr[1]))
        if type == 'p':
            p_type.append(tempStr[2])
        line = f.readline()
    f.close()
    if type == 'p':
        return x, y, p_type
    return x, y

def findDistance(x, y, pointX, pointY):
    '''对于输入的点计算与点组pointX, pointY中每个点的距离，并返回距离列表'''
    return(list(map(lambda tempx, tempy: ((x - tempx)**2 + (y - tempy)**2)**0.5, pointX, pointY)))

def countMax(list, p_typeValue):
    '''对临近的k个点计算其中类别数目最多的点，并返回该类别的值'''
    temp = 0
    for i in range(len(p_typeValue)):
        if list.count(p_typeValue[i]) > temp:
            temp = list.count(p_typeValue[i])
            value = p_typeValue[i]
    return value

def countWeightMax(list, p_typeValue, tempDistance):
    '''对临近的k个点计算其中加权值最大的类别，并返回该类别值'''
    temp = [0]*len(p_typeValue)
    for i in range(len(list)):
        temp[p_typeValue.index(list[i])] += 1/tempDistance[i]
    value = p_typeValue[temp.index(max(temp))]
    return value

def crossVerify(x, y, type):
    '''交叉验证'''
    tempP = [[[], [], []] for i in range(10)]
    tempT = [[[], [], []] for i in range(10)]
    minRate = 1
    minK = 1
    Rate = []
    num = int(len(x)/10) if len(x)%10 == 0 else int(len(x)/10 + 1)
    lack = num*10 - len(x)
    for i in range(10):#将数据固定分为十份，为了保证每份数目一致，在总数据量非10倍数时，有进行移位补位
        if i == 0:
            numStart = 0
        elif i <= lack:
            numStart = numEnd -1
        else:
            numStart = numEnd
        numEnd = numStart + num
        tempT[i][0], tempT[i][1], tempT[i][2] = x[numStart:numEnd], y[numStart:numEnd], type[numStart:numEnd]
        tempP[i][0], tempP[i][1], tempP[i][2] = x[0:numStart] + x[numEnd:len(x)], y[0:numStart] + y[numEnd:len(x)], type[0:numStart] + type[numEnd:len(x)]
    for k in range(1, int(len(x)**0.5)+1):#对于1到n的k值，进行后续操作，挑选出平均误差最小的k值进行返回（n为总数据量开根）
        errorRate = []
        for i in range(10):
            errorNum = 0
            tempType = KNN(tempP[i], tempT[i], k)#依次将十组数据，分为1：9，作为测试集和训练集，进行十次KNN运算，得出预测的分类值
            for j in range(num):
                if tempT[i][2][j] != tempType[j]:#根据预测的分类值与数据原本的分类值进行误差率的计算
                    errorNum += 1
            errorRate.append(float(errorNum)/float(num))
        Rate.append(sum(errorRate)/10)#用以后续展示各个k值的平均误差值，无实际作用，可删去
        if sum(errorRate)/10 < minRate:#找出最小的平均误差率，并返回其值minK
            minRate = sum(errorRate)/10
            minK = k
    print(Rate)
    print(minK)
    global FLAG#定义标志，表示已经找到合适的k值，后续再进行KNN运算即代表不用再返回分类结果，而是作图
    FLAG = 1
    return minK

def KNN(pFile, tFile, k):
    '''
    当k未赋值时，表示主程序，读取训练集和测试集，并将训练集代入进行交叉验证
    当k存在赋值时，表示正在交叉验证中执行，训练集的数据和测试集的数据，均由传入的参数得到，传入的参数为训练集的十个分组，9组作为训练集，1组作为测试集
    '''
    t_type = []
    p_typeSet = set()
    if k == '':
        p_x, p_y, p_type = loadData(pFile, 'p')
        t_x, t_y = loadData(tFile, 't')
        k = crossVerify(p_x, p_y, p_type)
    else:
        p_x, p_y, p_type = pFile[0], pFile[1], pFile[2]
        t_x, t_y = tFile[0], tFile[1]
    '''对所有数据的类别进行整理，整理出实际的数据分类种类'''
    for i in range(len(p_type)):
        p_typeSet.add(p_type[i])
        p_typeValue = list(p_typeSet)
    '''对每一个测试集中的数据，都计算与训练集中所有点的距离，并进行排序，找到距离最近的k个点,并将最邻近k个点的类别做记录'''
    for i in range(len(t_x)):#
        distance = findDistance(t_x[i], t_y[i], p_x, p_y)
        tempDistance = distance[:]
        tempDistance.sort(reverse=False)
        tempDistance = tempDistance[0:k]
        type = []
        for j in range(len(tempDistance)):
            type.append(p_type[distance.index(tempDistance[j])])
        '''
        对点加权作为分类依据的方法。当测试集中某个点与训练集中某个点发生完全重合时，直接将训练集中该点的类别作为测试点的分类结果
        当未发生重合时，选取加权值最大的类别作为该点的分类结果
        '''
        if tempDistance[0] == 0:
            t_type.append(p_type[distance.index(0)])
        else:
            # t_type.append(countMax(type, p_typeValue))#计算点的个数作为分类依据的方法
            t_type.append(countWeightMax(type, p_typeValue, tempDistance))#对距离进行加权计算
    '''
    当标志为0时，代表正在用KNN进行交叉验证，返回得到的分类信息
    当标志为1时，代表正在对测试集进行分类，作图，并将分类结果写入result.txt文件
    '''
    if FLAG == 0:
        return t_type
    else:
        f = open('result.txt', mode='w', encoding='utf-8')
        for i in range(len(t_x)):
            plt.scatter(t_x[i], t_y[i], marker='x', color=color[p_typeValue.index(t_type[i])], s=100)
            f.write(str(t_x[i]) + ',' + str(t_y[i]) + ',' + str(t_type[i]) + '\n')
        f.close()
        for i in range(len(p_x)):
            plt.scatter(p_x[i], p_y[i], marker='o', color=color[p_typeValue.index(p_type[i])])
        plt.show()

if __name__=='__main__':
    KNN(sys.argv[1], sys.argv[2], '')
