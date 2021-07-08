from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User


def user_check(name: str, ps: str) -> bool:
    try:
        user = User.objects.get(username=name)
        # 检查纯文本密码和加密后的密码是否一致

        return check_password(ps, user.password)
    except User.DoesNotExist:
        return False
