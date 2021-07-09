from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User


def user_check(name: str, ps: str) -> bool:
    """
    判断是否用户名与密码一致
    当用户不存在或者用户名与密码不一致的时候，返回False
    否则返回True
    """
    try:
        user = User.objects.get(username=name)
        return check_password(ps, user.password)
    except User.DoesNotExist:
        return False
