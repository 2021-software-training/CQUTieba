from mainpage.models import Article, Comment, LikeList
from login.models import NumCounter, MyUser
from django.db.models.query import QuerySet
from login.token import check_token
from django.http import HttpResponse
from mainpage.models import Image


def user_authentication(request) -> dict:
    """
    用于检验用户的身份
    :param request:
    :return: {
        返回验证的结果和用户名
        "result": res[0],
        "username": res[1]
    }
    """
    token = request.META.get("HTTP_AUTHORIZATION")
    if (token is None) or (len(str(token)) < 5):
        return {
            "result": False,
            "username": None
        }
    res = check_token(token)
    return {
        "result": res[0],
        "username": res[1]
    }


def get_user_name(article:Article) -> str:
    my_user_id = article.author_id
    my_user = MyUser.objects.get(my_user_id=my_user_id)
    return my_user.user.username


def show_img(img_id):
    """
    展示图片
    :param img_id: 图片id
    :return: 图片URL
    """
    image = Image.objects.get(id=img_id)
    return str(image.img.url)