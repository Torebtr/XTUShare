# coding=utf-8
# @author : 0uLL
# @software : pycharm
from django.urls import path
from shareplat import views

urlpatterns = [
    path('main/',views.page_main,name='page_main'),  # 主界面
    path('login/',views.login,name='login'),     # 登陆界面
    path('logout/',views.logout,name='logout'),  # 登出
    path('register/', views.register, name='register'),  # 注册
    path('myarticle/<page_num>/',views.myarticle,name='myarticle'),
    path('create_article/', views.create_article,name='create_article'),
    path('delete_article/',views.delete_article,name='delete_article'),
    path('go_set_classify/',views.go_set_classify,name='go_set_classify'),
    path('set_classify/',views.set_classify,name='set_classify'),
    path('go_set_tags/',views.go_set_tags,name='go_set_tags'),
    path('set_tags/',views.set_tags,name='set_tags'),
    path('search_result/',views.search_result,name='search_result'),
]