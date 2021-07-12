import sys
import json
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus


class DemoError(Exception):
    pass


def fetch_token():
    """
    :return: token
    """
    # 固定参数
    API_KEY = 'Bpz6z5ek1KuvDMK0B4Tl289p'
    SECRET_KEY = 'RM23b0Z9cHqg4kqi47wIWmBnuPpZ28tb'
    TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
    SCOPE = 'audio_tts_post'

    print("fetch token begin")
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
        result_str = result_str.decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if 'access_token' in result.keys() and 'scope' in result.keys():
        if SCOPE not in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


def create_MP3(TEXT, PER=0, SPD=5, PIT=5, VOL=5, USR = 1):
    """
    :param TEXT: 需要转换的文本
    :param PER: 发音人, 0为度小美，1为度小宇，3为度逍遥，4为度丫丫
    :param SPD: 语速，取值0-15，默认为5中语速
    :param PIT: 音调，取值0-15，默认为5中语调
    :param VOL: 音量，取值0-9，默认为5中音量
    :param USR: 上传用户的信息编号
    :return:
    """
    # 固定参数
    AUE = 3  # 下载的文件格式, 3:mp3, 4:pcm-16k, 5:pcm-8k, 6:wav
    FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
    FORMAT = FORMATS[AUE]
    CUID = "123456PYTHON"
    TTS_URL = 'http://tsn.baidu.com/text2audio'
    LAN = 'zh'
    CTP = 1

    token = fetch_token()
    tex = quote_plus(TEXT)
    print(tex)
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
              'lan': LAN, 'ctp': CTP}

    data = urlencode(params)
    print('test on Web Browser' + TTS_URL + '?' + data)

    req = Request(TTS_URL, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()

        headers = dict((name.lower(), value) for name, value in f.headers.items())

        has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()
        has_error = True

    save_file = "error.txt" if has_error else 'Result{0}.'.format(USR) + FORMAT #按照上传人的令牌号储存
    with open('{0}'.format(save_file), 'wb') as of:
        #注意要修改
        of.write(result_str)

    if has_error:
        result_str = str(result_str, 'utf-8')
        print("tts api error:" + result_str)

    print("result saved as :" + save_file)
    return