from django.contrib import admin
from social.models import Socialusers
# Register your models here.

class UserInfoAdmin(admin.ModelAdmin):
    # 指定每页显示10条数据
    list_per_page = 10
    list_display = ['id', 'username', 'password', 'chinesename', 'email', 'qq', 'weibo', 'identity_number', 'cell_phone', 'ip_address', 'college', 'living_place', 'source', 'remarks']
    # 列表页右侧过滤栏
    list_filter = ['username']
    # 列表页上方的搜索框
    search_fields = ['username']

admin.site.register(Socialusers, UserInfoAdmin)