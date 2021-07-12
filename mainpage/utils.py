from mainpage.models import Article, Comment, LikeList
from login.models import NumCounter, MyUser
from django.db.models.query import QuerySet
from login.token import check_token
from django.http import HttpResponse


def user_authentication(request) -> dict:
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
