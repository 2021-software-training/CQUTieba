'''
本功能实现了计算出文本当中每个词语的词的权值
关键字抽取
'''
from jieba import analyse
tfidf=analyse.extract_tags
# 基于TF-IDF算法关键词提取
class tf_idf():
    def __init__(self,text):
        self.text = text
        self.words = []
        self.weight = []
    @property
    def keyword(self):
        tfidf=analyse.extract_tags
        keywords=tfidf(self.text,topK=10,withWeight=True)
        for i in keywords:
            self.words.append(i[0])
            self.weight.append(i[1])
