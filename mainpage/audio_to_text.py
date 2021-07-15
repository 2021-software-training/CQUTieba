# 需要baidu-aip
from aip import AipSpeech


def read_audio(filePath):
    """
    读入语音文件
    :param filePath
    :return
    """
    with open(filePath, 'rb') as fp:
        return fp.read()


def get_text(filePath, fileFormat='wav'):
    """
    :param filePath: 文件路径, 字符串格式, 不区分大小写
    :param fileFormat: 文件格式名(wav或pcm或amr)
    :return: 转文字结果
    """
    # 固定参数
    APP_ID = '24527560'
    API_KEY = 'Bpz6z5ek1KuvDMK0B4Tl289p'
    SECRET_KEY = 'RM23b0Z9cHqg4kqi47wIWmBnuPpZ28tb'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.asr(read_audio(filePath), fileFormat, 16000, {'dev_pid': 1537, })
    """
    result
    {
        err_msg: 错误码描述
        err_no: 错误码
        sn: 语音数据唯一标识码
        result: 转文字结果列表
    }
    """
    return result["result"][0]