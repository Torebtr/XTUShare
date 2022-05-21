# coding=utf-8
# @author : 0uLL
# @software : pycharm
from django.urls import path
from shareplat import views

urlpatterns = [
    path('main/',views.page_main,name='page_main'),  # 主界面
    path('login/',views.login,name='login'),     # 登陆界面
    path('register/', views.register, name='register'),  # 注册
]