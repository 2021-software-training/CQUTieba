import requests

from urllib.parse import urlencode


def fetch_token():
    """
    获得token
    :return: access_token
    """
    appID = '24528904'
    api_key = 'GCnu6TNETwGmKdKeM3RSlY3Z'
    secret_key = 'qeoyStuzwheKndAQsvb5HHbUy4SPIbaB'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' \
           + api_key + '&client_secret=' + secret_key
    response = requests.get(host)
    if response:
        print(response.json())
    return response.json()['access_token']


def face_register(image, user_id):
    """
    人脸注册
    :param image: 图片URL
    :param user_id: 用户ID
    :return: 返回值信息
    """
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
    params = {
        'image': image,
        'image_type': "URL",
        'group_id': "default",
        'user_id': str(user_id),
        'user_info': "",
        'quality_control': "LOW",
        'liveness_control': "NORMAL",
    }
    access_token = fetch_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    data = urlencode(params)
    response = requests.post(request_url, data=data, headers=headers)
    if response:
        print(response.json())
    return response.json()


def face_update(image, user_id):
    """
    人脸信息更新
    :param image: 图片URL
    :param user_id: 用户ID
    :return: 返回值信息
    """
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/update"
    params = {
        'image': image,
        'image_type': "URL",
        'group_id': "default",
        'user_id': str(user_id),
        'user_info': "",
        'quality_control': "LOW",
        'liveness_control': "NORMAL",
    }
    access_token = fetch_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    data = urlencode(params)
    response = requests.post(request_url, data=data, headers=headers)
    if response:
        print(response.json())
    return response.json()


def face_search(image):
    """
    人脸查询
    :param image: 图片URL
    :return:
    """
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
    params = {
        'image': image,
        'image_type': "URL",
        'group_id': "default",
        'quality_control': "LOW",
        'liveness_control': "NORMAL",
    }
    access_token = fetch_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    data = urlencode(params)
    response = requests.post(request_url, data=data, headers=headers)
    if response:
        print(response.json())
    # response信息:
    # "face_token": 人脸token
    # "user_list": [
    #    {
    #       "group_id" : 用户组ID, 默认default
    #       "user_id": 用户ID
    #       "user_info": 用户信息
    #       "score": 匹配得分
    #     }]
    if response.json()['user_list'][0]["score"] > 85:
        return response.json()['user_list'][0]["user_id"]
