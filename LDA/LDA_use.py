import json
import os
import jieba_fast as jieba
import gensim
from gensim import corpora

jieba.load_userdict("F:/代码code/DSTS/dict/dict_baidu_utf8.txt")
jieba.load_userdict("F:/代码code/DSTS/dict/dict_pangu.txt")
jieba.load_userdict("F:/代码code/DSTS/dict/dict_sougou_utf8.txt")
jieba.load_userdict("F:/代码code/DSTS/dict/dict_tencent_utf8.txt")
jieba.load_userdict("F:/代码code/DSTS/dict/my_dict.txt")
stopwords = []  # 创建停用词列表
for line in open('F:/代码code/DSTS/dict/Stopword.txt', encoding='UTF-8'):
    x = line.split('\n')[0]
    stopwords.append(x)


def LDA_topic(text):
    vector = []
    seg_list = jieba.lcut(text, cut_all=False)  # 使用分词，将文本分开 生成列表
    result = []
    for j in seg_list:  # 去掉停用词
        if j not in stopwords and j is not ' ':
            result.append(j)
    result = [result]
    dictionary = corpora.Dictionary(result)  # 构造词典，给每一个词创建一个索引号
    # 使用上面的词典，将转换文档列表（语料）变成 DT 矩阵
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in result]
    model = gensim.models.LdaModel.load('F:/代码code/DSTS/LDA/lda.model')  # 加载训练好的模型
    for e, values in enumerate(model.inference(doc_term_matrix)[0]):
        for ee, value in enumerate(values):
            vector.append(value)
    return vector


if __name__ == '__main__':
    with open("../rumor/4473713031.json", 'r', encoding='UTF-8')as f:
        weibo_centent = f.read()
        weibo_dict = json.loads(weibo_centent)  # 将 JSON 对象转换为 Python 字典
        for i in range(0, len(weibo_dict)):
            item = weibo_dict[i]
            text1 = item['text']  # 逐条提取微博正文
            LDA_topic(text1)
