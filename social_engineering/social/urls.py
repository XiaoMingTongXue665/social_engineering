from django.urls import path
from social import views

urlpatterns = [
    path(r'', views.index, name='index'), # 自动跳转到index首页
    path(r'index/', views.index, name='index'),
]
