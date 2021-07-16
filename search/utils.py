'''
这里实现了：
1.lcs，判定出是否为完全字串
2.分词，并可以从中去掉所有的标点符号
3.抽取文本中的关键词并对他们进行权值检索
4.局部敏感哈希，计算两文本的相似度
'''
import jieba as jb
from jieba import analyse
from math import exp
jb.setLogLevel(jb.logging.INFO)
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
                 '〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。:' \
                 '( ) / * .'
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
    #我们只抽取文本的10个关键词
    weight,words = [],[]
    if(len(text)==1):
        weight= [1.0]
        words.append(text)
    for i in keywords:
        words.append(i[0])
        weight.append(i[1])
    return words,weight

class simhash:
    # 构造函数
    def __init__(self, tokens='', hashbits=128):
        self.hashbits = hashbits
        self.hash = self.simhash(tokens)

    # 生成simhash值
    def simhash(self, tokens):
        # v是长度128的列表
        v = [0] * self.hashbits
        tokens_hash = [self.string_hash(x) for x in tokens]
        for t in tokens_hash:  # t为token的普通hash值
            for i in range(self.hashbits):
                bitmask = 1 << i
                if t & bitmask:
                    v[i] += 1  # 查看当前bit位是否为1,是的话将该位+1
                else:
                    v[i] -= 1  # 否则的话,该位-1
        fingerprint = 0
        for i in range(self.hashbits):
            if v[i] >= 0:
                fingerprint += 1 << i
        return fingerprint  # 整个文档的fingerprint为最终各个位>=0的和

    # 求海明距离
    def hamming_distance(self, other):
        # 异或结果
        xorResult = (self.hash ^ other.hash)
        # 128个1的二进制串
        hashbit128 = ((1 << self.hashbits) - 1)
        x = xorResult & hashbit128
        count = 0
        while x:
            count += 1
            x &= x - 1
        return count

    # 求相似度
    def similarity(self, other):
        a = float(self.hash)
        b = float(other.hash)
        if a > b:
            return b / a
        else:
            return a / b

    # 针对source生成hash值
    def string_hash(self, source):
        if source == "":
            return 0
        else:
            result = ord(source[0]) << 7
            m = 1000003
            hashbit128 = ((1 << self.hashbits) - 1)

            for c in source:
                temp = (result * m) ^ ord(c)
                result = temp & hashbit128

            result ^= len(source)
            if result == -1:
                result = -2

            return result

if __name__ == '__main__':
    s = '你 知道 里约 奥运会，媒体 玩出了 哪些 新花样？'
    print(s.split())
    hash1 = simhash(s.split())
    print (hash1.__str__())
    s = '我 知道 里约 奥运会，媒体 玩出了 哪些 新花样'
    hash2 = simhash(s.split())
    print (hash2.__str__())
    s = '视频 直播 全球 知名 媒体 的 战略 转移'
    hash3 = simhash(s.split())

    print("   ", hash1.similarity(hash2))
    print( "   ", hash1.similarity(hash3))
    print("   ", hash2.similarity(hash3))
    s = cut('地狱模式:国内读完传统工科本科(非CS/EE), 本科期间拿下ACM金, '
              '本科毕业进谷歌上海困难模式:国内普通本科毕业, 美国一般学校排名硕士, '
              '刷题2000号称刷爆Leetcode, 毕业拿到谷歌面试并且成功拿到offer中等困难模式(三选一):'
              '国内普通本科毕业, 美国著名CS学校CS专业硕士(要求不高嘛Purdue那一级别及以上即可), '
              '(研究生第一个暑假前)刷题2000号称刷爆Leetcode, 拿到谷歌实习并拿到return offer, '
              '毕业return offer面试成功拿到offer国内普通本科毕业, 美国著名CS学校CS专业硕士'
              '(要求不高嘛Purdue那一级别及以上即可), 毕业拿到湾区某厂offer,从事CS工作, '
              '(上班期间)刷题2000号称刷爆Leetcode, 拿到谷歌社招面试,成功拿到offer入职国内'
              'Top10 CS本科毕业, 美国CS相关专业进修博士, (毕业前有1+个google/FAIR等类似实习), '
              '成功拿到return offer(并且return次数能够抵掉面试), '
              '毕业return offer拿到offer这个问题问偏了, 重点不是难度, '
              '是要对加入谷歌有个正确的期望值. 强如谷歌也是你说的“压力很大,吃年轻饭”的”学'
              '计算机的高材生毕业当了程序员或码农“搭起来的, 在台前出风头的是少数, 幕后是全球各路天才的汗水.'
              ' Talk is cheap, show me the f**king code.')
    hash2.simhash(s)
    print(hash2.similarity(hash3))

