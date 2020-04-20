
from django.urls import path
from login import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    # 邮件确认请求
    path('confirm/', views.user_confirm, name='confirm'),
]