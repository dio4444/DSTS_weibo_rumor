import json
from city import City


def user_analysis(filename):
    with open(filename, 'r', encoding='UTF-8')as f:
        weibo_centent = f.read()
        weibo_dict = json.loads(weibo_centent)  # 将 JSON 对象转换为 Python 字典
        # 每一个JSON对象都是一个事件，转换成的列表里的每一个字典都是一条相关微博
        start_time = (weibo_dict[0])['t']
        ternimal_time = (weibo_dict[-1])['t']
        N = 10
        interval = ((ternimal_time-start_time)/N)
        feature_vector = []
        x = []
        for a in range(0, len(weibo_dict)):
            vector = []
            item = weibo_dict[a]
            time = item['t']  # 转发时间
            stamp = int((time - start_time) / interval)
            if stamp == N:  # 正好取到了端点值，将端点值归到最后一个区间
                stamp = (N-1)  # 得到时间戳
            vector.append(stamp)
            # #########################微博的用户特征
            if item['user_description'] is not '':  # 用户个人介绍
                vector.append(1)
            else:
                vector.append(0)

            if item['verified'] is 'True':  # 是否是微博认证用户，即加V用户，True：是，False：否
                vector.append(1)
            else:
                vector.append(0)

            vector.append(item['verified_type'])  # 认证类型
            if item['gender'] is 'm':  # 性别，m：男、f：女、n：未知
                vector.append(1)
            elif item['gender'] is 'f':
                vector.append(0)
            elif item['gender'] is 'n':
                vector.append(0.5)

            vector.append(City(int(item['province']), int(item['city'])))  # 是否是大城市
            friends_count = item['friends_count']
            vector.append(friends_count)  # 关注数
            followers_count = item['followers_count']
            vector.append(followers_count)  # 粉丝数

            vector.append(item['statuses_count'])  # 微博数（该用户发的）

            time1 = item['t']
            time2 = item['user_created_at']
            vector.append(int((time1 - time2) / 86400))  # 用户建号时间,单位：天

            if friends_count == 0:
                vector.append(0)  # reputation score of users
            else:
                vector.append(followers_count / friends_count)  # reputation score of users

            x.append(vector)

        flag = 0  # 时间戳标记
        # 初始化中间变量列表
        temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # 变量容器记录第一条微博的特征
        temp[0] = (x[0])[0]
        temp[1] = (x[0])[1]
        temp[2] = (x[0])[2]
        if (x[0])[3] == -1:  # 普通用户
            temp[3] += 1
        elif (x[0])[3] == 0:  # 名人
            temp[4] += 1
        elif (x[0])[3] == 1:  # 政府
            temp[5] += 1
        elif (x[0])[3] == 2:  # 企业
            temp[6] += 1
        elif (x[0])[3] == 3:  # 媒体
            temp[7] += 1
        elif (x[0])[3] == 4:  # 校园
            temp[8] += 1
        elif (x[0])[3] == 5:  # 网站
            temp[9] += 1
        elif (x[0])[3] == 6:  # 应用
            temp[10] += 1
        elif (x[0])[3] == 7:  # 团体（机构）
            temp[11] += 1
        elif (x[0])[3] == 8:  # 待审企业
            temp[12] += 1
        elif (x[0])[3] == 200:  # 初级达人
            temp[13] += 1
        elif (x[0])[3] == 220:  # 中高级达人
            temp[14] += 1
        elif (x[0])[3] == 400:  # 已故V用户
            temp[15] += 1
        temp[16] = x[0][4]
        temp[17] = x[0][5]
        temp[18] = x[0][6]
        temp[19] = x[0][7]
        temp[20] = x[0][8]
        temp[21] = x[0][9]
        temp[22] = x[0][10]
        count = 1  # 计数
        for weibo in x[1:]:  # 从第二个开始遍历
            if weibo[0] == flag:  # 同一个时间戳内
                temp[0] = flag
                temp[1] += weibo[1]  # 提供个人介绍
                temp[2] += weibo[2]  # 认证
                if weibo[3] == -1:  # 普通用户
                    temp[3] += 1
                elif weibo[3] == 0:  # 名人
                    temp[4] += 1
                elif weibo[3] == 1:  # 政府
                    temp[5] += 1
                elif weibo[3] == 2:  # 企业
                    temp[6] += 1
                elif weibo[3] == 3:  # 媒体
                    temp[7] += 1
                elif weibo[3] == 4:  # 校园
                    temp[8] += 1
                elif weibo[3] == 5:  # 网站
                    temp[9] += 1
                elif weibo[3] == 6:  # 应用
                    temp[10] += 1
                elif weibo[3] == 7:  # 团体（机构）
                    temp[11] += 1
                elif weibo[3] == 8:  # 待审企业
                    temp[12] += 1
                elif weibo[3] == 200:  # 初级达人
                    temp[13] += 1
                elif weibo[3] == 220:  # 中高级达人
                    temp[14] += 1
                elif weibo[3] == 400:  # 已故V用户
                    temp[15] += 1
                temp[16] += weibo[4]  # 性别 m:1 f:0 n:-1
                temp[17] += weibo[5]  # 是否是大城市
                temp[18] += weibo[6]  # 关注
                temp[19] += weibo[7]  # 粉丝
                temp[20] += weibo[8]  # 微博数
                temp[21] += weibo[9]  # 建号时间
                temp[22] += weibo[10]  # 影响因子
                count += 1
            else:  # 时间戳改变
                for a in range(1,23):
                    temp[a] = temp[a] / count
                feature_vector.append(temp[1:])

                if weibo[0] != (flag + 1):  # 时间戳不连续，需要补0向量
                    for a in range(weibo[0]-flag-1):
                        temp = [flag+1]+[0]*22  # 时间戳 和 22个0
                        flag += 1
                        if flag == (N-1):  # 如果(N-1)也需要补0向量，那么这一条不执行添加，因为最后必定会有一条不是0
                            break
                        feature_vector.append(temp[1:])
                if flag == (N-1):  # 如果时间戳改变成了(N-1)，那么后面的所有微博都添加在这个时间戳内
                    # 改变时间戳标记，改变中间变量容器
                    temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    count = 0
                    # 找到当前微博
                    p = x.index(weibo)
                    for thing in x[p:]:
                        temp[0] = flag
                        temp[1] += thing[1]  # 提供个人介绍
                        temp[2] += thing[2]  # 认证
                        if thing[3] == -1:  # 普通用户
                            temp[3] += 1
                        elif thing[3] == 0:  # 名人
                            temp[4] += 1
                        elif thing[3] == 1:  # 政府
                            temp[5] += 1
                        elif thing[3] == 2:  # 企业
                            temp[6] += 1
                        elif thing[3] == 3:  # 媒体
                            temp[7] += 1
                        elif thing[3] == 4:  # 校园
                            temp[8] += 1
                        elif thing[3] == 5:  # 网站
                            temp[9] += 1
                        elif thing[3] == 6:  # 应用
                            temp[10] += 1
                        elif thing[3] == 7:  # 团体（机构）
                            temp[11] += 1
                        elif thing[3] == 8:  # 待审企业
                            temp[12] += 1
                        elif thing[3] == 200:  # 初级达人
                            temp[13] += 1
                        elif thing[3] == 220:  # 中高级达人
                            temp[14] += 1
                        elif thing[3] == 400:  # 已故V用户
                            temp[15] += 1
                        temp[16] += thing[4]  # 性别 m:1 f:0 n:-1
                        temp[17] += thing[5]  # 是否是大城市
                        temp[18] += thing[6]  # 关注
                        temp[19] += thing[7]  # 粉丝
                        temp[20] += thing[8]  # 微博数
                        temp[21] += thing[9]  # 建号时间
                        temp[22] += thing[10]  # 影响因子
                        count += 1

                    break
                flag = weibo[0]  # 改变时间戳标记，改变中间变量容器
                temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                temp[0] = flag
                temp[1] = weibo[1]
                temp[2] = weibo[2]
                if weibo[3] == -1:  # 普通用户
                    temp[3] += 1
                elif weibo[3] == 0:  # 名人
                    temp[4] += 1
                elif weibo[3] == 1:  # 政府
                    temp[5] += 1
                elif weibo[3] == 2:  # 企业
                    temp[6] += 1
                elif weibo[3] == 3:  # 媒体
                    temp[7] += 1
                elif weibo[3] == 4:  # 校园
                    temp[8] += 1
                elif weibo[3] == 5:  # 网站
                    temp[9] += 1
                elif weibo[3] == 6:  # 应用
                    temp[10] += 1
                elif weibo[3] == 7:  # 团体（机构）
                    temp[11] += 1
                elif weibo[3] == 8:  # 待审企业
                    temp[12] += 1
                elif weibo[3] == 200:  # 初级达人
                    temp[13] += 1
                elif weibo[3] == 220:  # 中高级达人
                    temp[14] += 1
                elif weibo[3] == 400:  # 已故V用户
                    temp[15] += 1
                temp[16] += weibo[4]  # 性别 m:1 f:0 n:-1
                temp[17] += weibo[5]  # 是否是大城市
                temp[18] += weibo[6]  # 关注
                temp[19] += weibo[7]  # 粉丝
                temp[20] += weibo[8]  # 微博数
                temp[21] += weibo[9]  # 建号时间
                temp[22] += weibo[10]  # 影响因子
                count = 1

        for a in range(1, 23):  # 添加进这个事件的最后一条微博
            temp[a] = temp[a] / count
        feature_vector.append(temp[1:])
    return feature_vector


if __name__ == '__main__':
    z = (user_analysis('rumor/11084174628.json'))
    for i in range(len(z)):
        print(z[i])
    print(len(z))