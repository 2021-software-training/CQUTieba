from audio import  *
from django.test import TestCase
import sys
import os
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CQUTieba.settings')
django.setup()
class audioInfo():#语音的信息
    """
        :param PER: 发音人, 0为度小美，1为度小宇，3为度逍遥，4为度丫丫
        :param SPD: 语速，取值0-15，默认为5中语速
        :param PIT: 音调，取值0-15，默认为5中语调
        :param VOL: 音量，取值0-9，默认为5中音量
        :return:
    """
    def __init__(self,PER,SPD,PIT,VOL):
        self.PER = PER
        self.SPD = SPD
        self.PIT = PIT
        self.VOL = VOL
    def add_audio(self,text,USER):
        create_MP3(text,self.PER,self.SPD,self.PIT,self.VOL,USER)
if __name__=='__main__':
    PER=5
    SPD=3
    PIT=3
    VOL=3
    audio_this=audioInfo(PER=PER,
                         SPD=SPD,
                         PIT=PIT,
                         VOL=VOL)
    create_MP3("你好世界",5,3,3,3,15)
    #audio_this.add_audio("你好世界",15)
