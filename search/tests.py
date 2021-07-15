from django.test import TestCase

# Create your tests here.
import jieba
text = "征战四海只为今日一胜，我不会再败了。"
# jieba.cut直接得到generator形式的分词结果
seg = jieba.lcut(text)
for j in seg:
    print(j,end=' ')