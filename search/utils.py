'''
这里实现了：
1.lcs，判定出是否为完全字串
2.分词，并可以从中去掉所有的标点符号
'''
import jieba as jb
from jieba import analyse
from math import exp
def lcs(str1,str2):
    '''
    :param str1:用户输入的字符串
    :param str2: 匹配上去的字符串
    :return:
    '''
    dp=[[0 for i in range(len(str2)+1)] for j in range(len(str1)+1)]
    #dp[i][j]的意义是:当str1为i个单词,str2为j个单词的时候的最长连续子序列长度(记录在案)
    a,b=len(str1),len(str2)
    str1='a'+str1
    str2='a'+str2
    if len(str1)>len(str2):
        return False
    elif str1==str2:
        return True
    else:
        for i in range(1,a+1):
            for j in range(1,b+1):
                if str1[i]==str2[j]:
                    dp[i][j]=dp[i-1][j-1]+1
                else:
                    dp[i][j]=0
                if dp[i][j]==a:
                    return True
        return False
'''
 分词，去掉当中的标点符号
'''
punctuation_str ='＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、' \
                 '〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'
#记录在案的中文标点符号
def cut(text):
    '''
    :param text:输入的文本
    :return:所有标点符号均已删除的列表
    '''
    cutten = jb.lcut(text)
    for i in cutten:
        if i in punctuation_str:
            cutten.remove(i)
    return cutten
def get_weight_and_keyword(text):
    tfidf=analyse.extract_tags
    keywords=tfidf(text,topK=10,withWeight=True)
    weight,words = [],[]
    if(len(text)==1):
        weight= [1.0]
        words.append(text)
    for i in keywords:
        words.append(i[0])
        weight.append(i[1])
    return words,weight