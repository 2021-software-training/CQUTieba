import random
import math


def recommend(views,up_number,article_comments,age,i=1.0):#views是浏览量，up_number是点赞数，article_comments是评论数
    r = random.uniform(0.9, 1.1)  # 取得一个在（0.9~1.1的随机数）
    a = math.ceil(age)  # 对age向上取整
    s = 0.14 * 1/1500*views + 0.24 *1/15* up_number + 0.62 * article_comments  # 分子
    if(s!=0):
        w = s * r / (a ** i)
    else:
         w=0   
    return w


print('权重值为：',recommend(10000,2000,500,1))
