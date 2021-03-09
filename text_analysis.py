import json
import jieba_fast as jieba
import re
from LDA.LDA_use import LDA_topic


jieba.load_userdict("F:/代码code/DSTS/dict/dict_baidu_utf8.txt")
jieba.load_userdict("F:/代码code/DSTS/dict/dict_pangu.txt")
jieba.load_userdict("F:/代码code/DSTS/dict/dict_sougou_utf8.txt")
jieba.load_userdict("F:/代码code/DSTS/dict/dict_tencent_utf8.txt")
jieba.load_userdict("F:/代码code/DSTS/dict/my_dict.txt")

stopwords = []  # 创建停用词列表
for line in open('F:/代码code/DSTS/dict/Stopword.txt', encoding='UTF-8'):
    k = line.split('\n')[0]
    stopwords.append(k)
with open('emotion_analysis/negative_word.txt', encoding='UTF-8')as neg:
    with open('emotion_analysis/positive_word.txt', encoding='UTF-8')as pos:
        neg_dict = []  # 创建消极词典
        pos_dict = []  # 创建积极词典
        for line in neg:
            neg_dict.append(line.split('\n')[0])
        for line in pos:
            pos_dict.append(line.split('\n')[0])

with open('emotion_analysis/emo_neg.txt', encoding='UTF-8')as neg:
    with open('emotion_analysis/emo_pos.txt', encoding='UTF-8')as pos:
        neg_emot = []  # 创建消极表情库
        pos_emot = []  # 创建积极表情库
        for line in neg:
            neg_emot.append(line.split('\n')[0])
        for line in pos:
            pos_emot.append(line.split('\n')[0])


def text_analysis(filename):
    with open(filename, 'r', encoding='UTF-8')as f:
        weibo_centent = f.read()
        weibo_dict = json.loads(weibo_centent)  # 将 JSON 对象转换为 Python 字典
        # 每一个JSON对象都是一个事件，转换成的列表里的每一个字典都是一条相关微博
        start_time = (weibo_dict[0])['t']
        ternimal_time = (weibo_dict[-1])['t']
        N = 10
        interval = ((ternimal_time-start_time)/N)
        feature_vector = []
        x = []  # 记录中间变量
        for i in range(0, len(weibo_dict)):
            item = weibo_dict[i]  # 从头开始遍历事件集
            time = item['t']  # 转发时间
            stamp = int((time - start_time) / interval)
            if stamp == N:  # 正好取到了端点值，将端点值归到最后一个区间
                stamp = (N-1)  # 得到时间戳
            # #########################微博的内容特征
            text = item['text']  # 文本

            length = len(text)  # 文本长度
            hashtags_list = re.findall("#(.*)#", text)  # 提取标签，返回列表
            hashtags = len(hashtags_list)  # 返回标签数
            emoticons = re.findall("\[(.*?)\]", text)  # 提取表情，返回列表
            neg_emot_count = 0
            pos_emot_count = 0
            for emot in emoticons:  # 统计情感表情
                if emot in neg_emot:
                    neg_emot_count += 1
                elif emot in pos_emot:
                    pos_emot_count += 1
            url = text.count('http://')  # 统计出现网址个数
            at_mention = text.count('@')  # 统计 @ 行为
            username = re.findall('@(.*?) ', text)  # 用正则表达式提取@用户名
            for item in username:  # 将用户名删除
                text = (text.replace(item, ''))
            exclamation_marks = text.count('!') + text.count('！')  # !数量
            question_marks = text.count('?') + text.count('？')  # ?数量
            if exclamation_marks == 0:
                question_exclamation = 0
            else:
                question_exclamation = question_marks / exclamation_marks  # 比值
            seg_list = jieba.lcut(text, cut_all=False)  # 使用分词，将文本分开 生成列表
            pos_word_count = 0  # 正面词数量
            neg_word_count = 0  # 负面词数量
            first_person_pronouns = 0  # 第一人称代词数，因为第一人称代词基本上是停用词，故应该在文本内查找
            for word in seg_list:
                if (word == '我' or word == '我们' or word == '俺' or word == '咱'
                        or word == '小生' or word == '吾' or word == '吾辈' or word
                        == '在下' or word == '老夫' or word == '余' or word == '鄙人'
                        or word == 'I' or word == 'me' or word == 'we' or word ==
                        'us' or word == 'We'):
                    first_person_pronouns += 1
            result = []
            for k in seg_list:  # 去掉停用词
                if k not in stopwords:
                    result.append(k)
            for word in result:  # 统计情感词汇数量
                if word in neg_dict:
                    neg_word_count += 1
                elif word in pos_dict:
                    pos_word_count += 1
            sentiment_score = pos_emot_count + pos_word_count - neg_emot_count - neg_word_count  # 情绪得分
            topic = LDA_topic(result)
            vector = [stamp, interval, length, sentiment_score, url, pos_emot_count,
                      neg_emot_count, first_person_pronouns,hashtags, at_mention,
                      question_marks, exclamation_marks, question_exclamation] + topic

            x.append(vector)
        flag = 0  # 时间戳标记
        temp = x[0]  # 变量容器记录第一条
        count = 1  # 记录数量
        for weibo in x[1:]:  # 从第二个开始遍历
            if weibo[0] == flag:  # 同一个时间戳内
                temp[0] = flag
                temp[1] = interval
                for a in range(2, 31):
                    temp[a] += weibo[a]
                count += 1
            else:  # 时间戳改变
                for a in range(2, 31):
                    temp[a] = temp[a] / count
                feature_vector.append(temp)

                if weibo[0] != (flag + 1):  # 时间戳不连续，需要补0向量
                    for a in range(weibo[0]-flag-1):
                        temp = [flag+1]+[interval]+[0]*11 + [1/18]*18  # 时间戳 区间间隔 和 11个0
                        flag += 1
                        if flag == (N-1):  # 如果(N-1)也需要补0向量，那么这一条不执行添加，因为最后必定会有一条不是0
                            break
                        feature_vector.append(temp)
                if flag == (N-1):  # 如果时间戳改变成了(N-1)，那么后面的所有微博都添加在这个时间戳内
                    # 改变时间戳标记，改变中间变量容器
                    temp = [0]*len(weibo)
                    count = 0
                    # 找到当前微博
                    p = x.index(weibo)
                    for thing in x[p:]:
                        temp[0] = flag
                        temp[1] = interval
                        for a in range(2, 31):
                            temp[a] += thing[a]
                        count += 1
                    break
                flag = weibo[0]  # 改变时间戳标记，改变中间变量容器
                temp = weibo
                count = 1
        for a in range(2, 31):  # 添加这个事件的最后一个时间戳到特征向量
            temp[a] = temp[a] / count
        feature_vector.append(temp)
    return feature_vector


if __name__ == '__main__':
    z = (text_analysis('rumor/4016873519.json'))

