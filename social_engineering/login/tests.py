# from django.test import TestCase
# import hashlib
# from SocialRelations_Web import settings
#
# def hash_code(s, salt=settings.SECRET_KEY): # 加点盐
#     h = hashlib.sha256()
#     s += salt
#     h.update(s.encode()) # update方法只接收bytes类型
#     return h.hexdigest()
#
#
# print(hash_code('z'))
from login.models import ConfirmString
import datetime

a = datetime.timedelta(7)
now = datetime.datetime.now()
print(a)
print(now-a)

confirm = ConfirmString.objects.get(user='zyg')
# c_time = confirm.c_time