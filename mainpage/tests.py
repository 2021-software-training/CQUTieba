from django.test import TestCase
import sys
import os
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CQUTieba.settings')
django.setup()
# Create your tests here.
#def create_MP3(TEXT, PER=0, SPD=5, PIT=5, VOL=5):
from mainpage.models import Article
from mainpage.utils import audioInfo
from django.core.files import File
from mainpage.audio import *
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
def get_audio(text,user_id):#生成文件
    """
        用于完成判定后要增加语音的功能
        :param PER: 发音人, 0为度小美，1为度小宇，3为度逍遥，4为度丫丫
        :param SPD: 语速，取值0-15，默认为5中语速
        :param PIT: 音调，取值0-15，默认为5中语调
        :param VOL: 音量，取值0-9，默认为5中音量
    """
    PER = 3
    SPD = 5
    PIT = 5
    VOL = 5
    audio_this = audioInfo(PER = PER,
                           SPD = SPD,
                           PIT = PIT,
                           VOL = VOL)
    audio_this.add_audio(text,user_id)
def add_article(add_authorID,
                add_articleText,
                add_articleAudio,
                add_chose_audio,
                add_articleTitle,
                add_articleType1,
                add_articleType2,
                add_articleType3,):
    """
    用于新增文章
    :param request: {
        articleID, authorId, articleText
            articleAudio(默认先不管这个 默认这个为空) articleTitle
                articleType1 articleType2 articleType3
        }
    :return: json形式的 {result: "yes"/"no"}
    """
    add_authorID = add_authorID
    add_articleText = add_articleText
    add_articleAudio = ""
    add_chose_audio = add_chose_audio#是否要上传声纹信息
    add_articleTitle = add_articleTitle
    add_articleType1 = add_articleType1
    add_articleType2 = add_articleType2
    add_articleType3 = add_articleType3
    #counter = NumCounter.objects.get(pk=1)
    article=Article(
        article_id="13",
        author_id=add_authorID,
        article_text=add_articleText,
        article_audio=add_articleAudio,
        article_chose_audio=add_chose_audio,
        article_title=add_articleTitle,
        article_type1=add_articleType1,
        article_type2=add_articleType2,
        article_type3=add_articleType3,
    )
    if add_chose_audio:
        get_audio(add_articleText,add_authorID)#生成文件并上传
        with open('Result{0}.mp3'.format(add_authorID),'rb') as f:
            article.article_audio.save('Reuslt{0}.mp3'.format(add_authorID),File(f))
            f.close()
    #counter.my_article_id += 1
    article.save()
    #article.objects.all().delete()
    os.remove('Result{0}.mp3'.format(add_authorID))
    f_list=os.listdir(os.getcwd())
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1]=='.mp3':
            os.remove(i)
    #上传之后立刻移除
if __name__=='__main__':
    ''' add_article(add_authorID=1628,add_articleText="你好世界",
                add_chose_audio=1,add_articleTitle="wryyyy",
                add_articleAudio="",add_articleType1="1",
                add_articleType2="2",add_articleType3="3")'''
    # 用split分割,分隔符.,从-1的位置(从右边开始)开始分割
'''
    def add_article(add_authorID,
                    add_articleText,
                    add_articleAudio,
                    add_chose_audio,
                    add_articleTitle,
                    add_articleType1,
                    add_articleType2,
                    add_articleType3,)
                    '''
