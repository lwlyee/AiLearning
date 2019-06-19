# -*- coding: UTF-8 -*-
import sys
import random

group = set()
randomfloat = lambda arg1, arg2: float('%.03f'%random.uniform(int(arg1), int(arg2)))

f = open('data.txt', mode='w+')
temp = '#' + sys.argv[1] + "," + sys.argv[2] + "," + sys.argv[3] + "," + sys.argv[4] + "," + sys.argv[5] + '\n'
f.write(str(temp))
f.close()

setlen = len(group)
while len(group) < int(sys.argv[5]):
    f = open('data.txt', mode='a')
    x = randomfloat(sys.argv[1], sys.argv[2])
    y = randomfloat(sys.argv[3], sys.argv[4])
    group.add((x, y))
    if setlen != len(group):
        f.write(str(x) + ',' + str(y) + '\n')
f.close()
