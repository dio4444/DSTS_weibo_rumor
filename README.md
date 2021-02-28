# -
读Ma 的文章后进行的复现工作，并进行了部分更改

使用的数据集：https://www.dropbox.com/s/46r50ctrfa0ur1o/rumdect.zip?dl=0

weibo_label 中的 weibo_id_label.txt 是数据集的标签

使用该标签对数据进行分类（由于6条标签和数据集中文件名不对应，故剔除）得到rumor、non_rumor文件夹


文本特征：

详细代码和注释见 text_analysis.py

LDA文件中的 LDA_train.pu 对数据集进行主题分类并保存训练模型

提取文本特征使用到 LDA_use.py ，用训练好的模型对文本分类


用户特征：

详细代码和注释见 user_analysis.py

调用了city.py 判断用户是否来自大城市。

城市大小：衡量中国城市的大小，以及决定城市影响力和辐射能力的，并不是取决于全域人口的多少，而主要取决于中心城区人口集聚规模的大小

根据新浪微博提供的省份城市编码表 https://open.weibo.com/wiki/%E7%9C%81%E4%BB%BD%E5%9F%8E%E5%B8%82%E7%BC%96%E7%A0%81%E8%A1%A8

和维基百科提供的中国大城市目录 


传播特征：

详细代码和注释见 propagation_analysis.py


时间序列：

这里只实现了论文中的SVM_DSTS_all，其他的可以自行修改

详细代码和注释见 DSTS.py


最终效果：

accuracy: 0.8027357633814762

precision: 0.9441549251954203

recall: 0.8027357633814762

F1 score: 0.8677210652998039


