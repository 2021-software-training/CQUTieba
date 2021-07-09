from datetime import datetime
class EmailVerifyRecord():#邮箱类别
    """
    图形验证码
    """
    def __init__(self,code='a',email="b",send_choice="regist",send_time=datetime.now()):
        self.code=code#验证码
        self.email=email#邮箱地址
        self.send_choice=send_choice#发送的需求
        self.send_time=send_time#注册的时间
    def __unicode__(self):
        return  '{0}({1})'.format(self.code, self.email)