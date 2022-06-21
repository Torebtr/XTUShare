# coding=utf-8
# @author : Torebtr
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
    path('edite_article/<article_id>/',views.edite_article,name='edite_article'),
    path('article_detail/<article_id>/',views.article_detail,name='article_detail'),
    path('go_set_classify/',views.go_set_classify,name='go_set_classify'),
    path('set_classify/',views.set_classify,name='set_classify'),
    path('go_set_tags/',views.go_set_tags,name='go_set_tags'),
    path('set_tags/',views.set_tags,name='set_tags'),
    path('search_result/',views.search_result,name='search_result'),
    path('library/',views.library,name='library'),
    path('search_author/',views.search_author,name='search_author'),
    path('search_tag/',views.search_tag,name='search_tag'),
    path('classify_manage/', views.classify_manage, name='classify_manage'),
    path('add_classify/', views.add_classify, name='add_classify'),
    path('add_tag/',views.add_tag,name='add_tag'),
    path('delete_classify/', views.delete_classify, name='delete_classify'),
    path('delete_tag/', views.delete_tag, name='delete_tag'),

    path('my_setting/',views.my_setting,name='my_setting'),

    path('verify/', views.verify, name='verify'),
    path('preview/<article_id>/',views.preview,name='preview'),
    path('back_article/',views.back_article,name='back_article'),
    path('verify_article/<article_id>/',views.verify_article,name='verify_article'),
    path('show_back_info/',views.show_back_info,name='show_back_info'),
    path('user_manage/<page_num>/',views.user_manage,name='user_manage'),
    path('add_user/',views.add_user,name='add_user'),
    path('edite_user/<user_id>/',views.edite_user,name='edite_user'),
    path('delete_user/',views.delete_user,name='delete_user'),
    path('change_password/',views.change_password,name='change_password'),
    path('delete_articles/',views.delete_articles,name='delete_articles'),
]