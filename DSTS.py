"""
一个事件的DSTS特征是由两部分组成的，
前半部分是每一个时间区间内的特征向量，
后半部分是相邻两个区间内的斜率
并且前半部分的特征向量要做归一化处理
最终得到的特征保存在同名txt文件中
"""

from text_analysis import text_analysis
from user_analysis import user_analysis
from propagation_analysis import propagation_analysis
import os
import concurrent.futures


def Z_score(feature):  # 对特征向量进行Z-score标准化
    # 求均值
    mean = [0] * len(feature[0])
    for a in range(len(feature)):
        for b in range(len(feature[0])):
            mean[b] += feature[a][b]
    for a in range(len(feature[0])):
        mean[a] = mean[a] / len(feature)
    sigma = [0] * len(feature[0])  # 求标准差
    for a in range(len(feature)):
        for b in range(len(feature[0])):
            sigma[b] += (feature[a][b] - mean[b]) ** 2
    for a in range(len(feature[0])):
        sigma[a] = (sigma[a] / len(feature)) ** 0.5
    for a in range(len(feature)):
        for b in range(len(feature[0])):
            feature[a][b] = 0 if sigma[b] == 0 else (feature[a][b] - mean[b]) / sigma[b]
    return feature


def function_1(rumor_file):  #
    t = text_analysis('rumor/' + rumor_file)
    u = user_analysis('rumor/' + rumor_file)
    p = propagation_analysis('rumor/' + rumor_file)
    l = []  # 记录特征向量
    slopes = []  # 记录斜率
    interval = t[0][1] / 3600  # 以小时为单位的区间间隔
    for i in range(len(t)):
        temp = t[i][2:] + u[i] + p[i]  # 将三种类型的向量合并到一个向量中
        l.append(temp)
    # 对特征向量进行Z-score标准化
    l = Z_score(l)
    for j in range(1, len(l)):
        slope = [(l[j][n] - l[j - 1][n]) / interval for n in range(len(l[0]))]
        slopes.append(slope)
    l = l + slopes  # 在特征向量后面添加斜率
    with open('feature1_10/' + rumor_file + '.txt', 'w')as f1:
        for item in l:
            for thing in item:
                f1.write(str(thing))
                f1.write(',')
            f1.write('\n')


def function_2(non_file):
    t = text_analysis('non_rumor/' + non_file)
    u = user_analysis('non_rumor/' + non_file)
    p = propagation_analysis('non_rumor/' + non_file)
    l = []  # 记录特征向量
    slopes = []  # 记录斜率
    interval = t[0][1] / 3600  # 以小时为单位的区间间隔
    for i in range(len(t)):
        temp = t[i][2:] + u[i] + p[i]  # 将三种类型的向量合并到一个向量中
        l.append(temp)
    # 对特征向量进行Z-score标准化
    l = Z_score(l)
    for j in range(1, len(l)):
        slope = [(l[j][n] - l[j - 1][n]) / interval for n in range(len(l[0]))]
        slopes.append(slope)
    l = l + slopes  # 在特征向量后面添加斜率
    with open('feature2_10/' + non_file + '.txt', 'w')as f2:
        for item in l:
            for thing in item:
                f2.write(str(thing))
                f2.write(',')
            f2.write('\n')


if __name__ == '__main__':
    rumor = os.listdir('rumor')
    non = os.listdir('non_rumor')
    with concurrent.futures.ProcessPoolExecutor() as executor:  # 并行化处理
        executor.map(function_1, rumor)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(function_2, non)
