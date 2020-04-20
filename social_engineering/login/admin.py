from django.contrib import admin
from login.models import UserProfile, ConfirmString

# Register your models here.

class UserInfoAdmin(admin.ModelAdmin):
    # 指定每页显示10条数据
    list_per_page = 10
    list_display = ['username', 'password', 'email', 'sex', 'c_time', 'has_confirmed']
    # 列表页右侧过滤栏
    list_filter = ['username']
    # 列表页上方的搜索框
    search_fields = ['username']

class ConfirmAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'c_time']

admin.site.register(UserProfile, UserInfoAdmin)



admin.site.register(ConfirmString, ConfirmAdmin)