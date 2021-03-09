import json
import os
import re

import jieba_fast as jieba
import gensim
from gensim import corpora


if __name__ == '__main__':
    jieba.load_userdict("../dict/dict_baidu_utf8.txt")
    jieba.load_userdict("../dict/dict_pangu.txt")
    jieba.load_userdict("../dict/dict_sougou_utf8.txt")
    jieba.load_userdict("../dict/dict_tencent_utf8.txt")
    jieba.load_userdict("../dict/my_dict.txt")
    stopwords = []  # 创建停用词列表
    for line in open('../dict/Stopword.txt', encoding='UTF-8'):
        x = line.split('\n')[0]
        stopwords.append(x)

    # 整合文档数据
    rumor = os.listdir('../rumor')
    non = os.listdir('../non_rumor')
    doc_complete = []
    print('开始加载谣言数据集数据：')
    for doc in rumor:
        if rumor.index(doc) % 400 == 0:
            print('已完成', 100 * rumor.index(doc)/len(rumor), '%')
        with open("../rumor/" + doc, 'r', encoding='UTF-8')as f:
            weibo_centent = f.read()
            weibo_dict = json.loads(weibo_centent)  # 将 JSON 对象转换为 Python 字典
            for i in range(0, len(weibo_dict)):
                item = weibo_dict[i]
                text = item['text']  # 逐条提取微博正文
                username = re.findall('@(.*?) ', text)  # 用正则表达式提取@用户名
                for item in username:  # 将用户名删除
                    text = (text.replace(item, ''))
                seg_list = jieba.lcut(text, cut_all=False)  # 使用分词，将文本分开 生成列表
                result = []
                for j in seg_list:  # 去掉停用词
                    if j not in stopwords and j is not ' ':
                        result.append(j)
                if len(result) >= 10:
                    doc_complete.append(result)  # 把一条微博的正文分词结果添加进文档列表内
    print('谣言数据集加载完毕，开始加载非谣言数据集：')
    for doc in non:
        if non.index(doc) % 400 == 0:
            print('已完成', 100 * non.index(doc)/len(non), '%')
        with open("../non_rumor/" + doc, 'r', encoding='UTF-8')as f:
            weibo_centent = f.read()
            weibo_dict = json.loads(weibo_centent)  # 将 JSON 对象转换为 Python 字典
            for i in range(0, len(weibo_dict)):
                item = weibo_dict[i]
                text = item['text']  # 逐条提取微博正文
                username = re.findall('@(.*?) ', text)  # 用正则表达式提取@用户名
                for item in username:  # 将用户名删除
                    text = (text.replace(item, ''))
                seg_list = jieba.lcut(text, cut_all=False)  # 使用分词，将文本分开 生成列表
                result = []
                for j in seg_list:  # 去掉停用词
                    if j not in stopwords and j is not ' ':
                        result.append(j)
                if len(result) >= 10:
                    doc_complete.append(result)  # 把一条微博的正文分词结果添加进文档列表内
    print('非谣言数据加载完毕')
    print('共计', len(doc_complete), '条文本')
    print('开始进行模型训练')
    dictionary = corpora.Dictionary(doc_complete)  # 构造词典，给每一个词创建一个索引号
    # 使用上面的词典，将转换文档列表（语料）变成 DT 矩阵
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_complete]
    # 使用 gensim 来创建 LDA 模型对象
    Lda = gensim.models.ldamodel.LdaModel

    # # 在 DT 矩阵上运行和训练 LDA 模型
    ldamodel = Lda(doc_term_matrix, num_topics=18, id2word=dictionary, passes=20)
    ldamodel.save('lda.model')
    print('模型训练完毕')
    # print(ldamodel.inference(doc_term_matrix))
    #
    # for e, values in enumerate(ldamodel.inference(doc_term_matrix)[0]):
    #     print(doc_complete[e])
    #     for ee, value in enumerate(values):
    #         print('\t主题%d推断值%.2f' % (ee, value))



