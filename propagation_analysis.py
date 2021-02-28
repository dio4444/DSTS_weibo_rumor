import json


def propagation_analysis(filename):
    with open(filename, 'r', encoding='UTF-8')as f:
        weibo_centent = f.read()
        weibo_dict = json.loads(weibo_centent)  # 将 JSON 对象转换为 Python 字典
        # 每一个JSON对象都是一个事件，转换成的列表里的每一个字典都是一条相关微博
        start_time = (weibo_dict[0])['t']
        ternimal_time = (weibo_dict[-1])['t']
        N = 10
        interval = ((ternimal_time - start_time) / N)
        x = []  # 记录中间变量
        feature_vector = []
        for i in range(0, len(weibo_dict)):
            vector = []
            item = weibo_dict[i]
            time = item['t']  # 转发时间
            stamp = int((time - start_time) / interval)
            if stamp == N:  # 正好取到了端点值，将端点值归到最后一个区间
                stamp = (N-1)  # 得到时间戳
            vector.append(stamp)
            # #########################微博的传播特征
            vector.append(item['comments_count'])  # 评论数
            vector.append(item['reposts_count'])  # 转发数
            x.append(vector)
        flag = 0  # 时间戳标记
        temp = (x[0])  # 变量容器记录第一条
        temp.append(1)
        for weibo in x[1:]:  # 从第二个开始遍历

            if weibo[0] == flag:  # 同一个时间戳内
                temp[0] = flag
                temp[1] += weibo[1]
                temp[2] += weibo[2]
                temp[3] += 1
            else:  # 时间戳改变
                temp[1] = temp[1] / temp[3]
                temp[2] = temp[2] / temp[3]
                feature_vector.append(temp[1:])

                if weibo[0] != (flag + 1):  # 时间戳不连续，需要补0向量
                    for a in range(weibo[0] - flag - 1):
                        temp = [flag + 1] + [0] * 3  # 时间戳 和 3个0
                        flag += 1
                        if flag == (N-1):  # 如果(N-1)也需要补0向量，那么这一条不执行添加，因为最后必定会有一条不是0
                            break
                        feature_vector.append(temp[1:])
                if flag == (N-1):  # 如果时间戳改变成了(N-1)，那么后面的所有微博都添加在这个时间戳内
                    # 改变时间戳标记，改变中间变量容器
                    temp = [0, 0, 0, 0]
                    # 找到当前微博
                    p = x.index(weibo)
                    for thing in x[p:]:
                        temp[0] = flag
                        temp[1] += thing[1]
                        temp[2] += thing[2]
                        temp[3] += 1

                    break
                flag = weibo[0]  # 改变时间戳标记，改变中间变量容器
                temp = weibo
                temp.append(1)
        temp[1] = temp[1] / temp[3]  # 添加进这个事件的最后一条微博
        temp[2] = temp[2] / temp[3]
        feature_vector.append(temp[1:])
    return feature_vector


if __name__ == '__main__':
    z = (propagation_analysis('rumor/11084174628.json'))
    for i in range(len(z)):
        print(z[i])
    print(len(z))
