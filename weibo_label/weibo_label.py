import os
import re
import shutil
from natsort import natsorted

# # #################     把微博标签文件进行自然排序
# list = []
# files = os.listdir("Weibo")  # 得到文件夹下所有文件名称
# files = natsorted(files)  # 进行自然排序
# with open("weibo_id_label.txt", 'r')as f:
#     with open('Weibo_label.txt', 'w')as f1:
#         for line in f:
#             name = int(line.split(' ', 1)[0])
#             label = int(line.split(' ', 1)[1][0:1])
#             list.append((name , label))
# list = sorted(list,key = lambda x: x[0])
# print(list)
# with open('Weibo_label.txt','w')as f:
#     for item in list:
#         item = str(item).replace('(','').replace(')','')
#         f.write(item)
#         f.write('\n')
# f.close()
# # #################      自然排序结果为'Weibo_label.txt'

path = 'F:/代码code/DSTS/Weibo'
# os.mkdir('rumor')
# os.mkdir('non_rumor')
files = os.listdir(path)
files = natsorted(files)  # 进行自然排序
for line in open('Weibo_label.txt'):
    filename = line.split(',')[0]
    label = int(line.split(',')[1])
    if label is 0:
        shutil.move(path + filename + '.json', 'non_rumor')  # 移动到non_rumor 文件夹
    else:
        shutil.move(path + filename + '.json', 'rumor')  # 移动到rumor 文件夹

#  找不同
# with open('Weibo_label.txt')as f:
#     files = natsorted(os.listdir('Weibo'))
#     for line1,line2 in zip(f,files):
#         if not line1.split(',')[0] == line2.split('.')[0]:
#             print(line2 + '\t' + line1)
#  3007 3908051012383200, 0
#  3440 3910904557063718, 0
#  3450 3910919157368349, 0
#  3467 3911180017645937, 0
#  3692 3911633284223848, 0
#  4504 3919182560764692, 0

