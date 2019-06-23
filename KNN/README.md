#环境：python3
#如何运行
python g_data.py 0 20 0 10 50 3
python KNN data.txt test.txt 20

#生成50个x范围0-20，y范围0-10的随机点，并用kmeans分为3簇，标记后存储在data.txt文件中
#以data.txt的数据为训练集，对test.txt的数据进行标记   20为对20个临近点进行比较，即为k值
#后续将尝试用算法自动取更为合理的k值

