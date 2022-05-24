# Create your models here.
from django.db import models
from mdeditor.fields import MDTextField


class User(models.Model):    # 用户
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)      # md5加密后的结果
    email = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    # is_lock = models.BooleanField(default=False)
    # login_fail = models.IntegerField(default=0)
    # invitation_code = models.CharField(max_length=255,null=True,unique=True)
    invitation_user = models.IntegerField(null=True)
    create_time = models.DateTimeField(auto_now=False)
    # invitation_num = models.IntegerField(default=0)
    article_num = models.IntegerField(default=0)


class Classify(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,unique=True)
    create_time = models.DateTimeField(auto_now=True)


class Tag(models.Model):      # 文章标签
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True,unique=True)
    create_time = models.DateTimeField(auto_now=True)


class Update_log(models.Model):  # 上传日志
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now=True)
    content = MDTextField()


class Article(models.Model): # 文章
    id = models.AutoField(primary_key=True)
    classify = models.ForeignKey('Classify',on_delete=models.SET_NULL,null=True)
    tags = models.CharField(max_length=255,null=True)
    content = MDTextField()
    title = models.CharField(max_length=255,null=False)
    create_time = models.DateTimeField(null=False)
    update_time = models.DateTimeField(auto_now=False)
    author = models.ForeignKey('User',on_delete=models.SET_NULL,null=True)
    state = models.IntegerField(default=0)     # 3为发布 1为暂存 2为发送审核
    read_num = models.IntegerField(default=0)
    back_info = models.TextField(default='')
    type = models.IntegerField(default=0)
    article_link = models.TextField(default='',null=True)


class Tool(models.Model):  # 工具
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255,null=False)
    path = models.CharField(max_length=255,null=False)  # 静态资源路由
    upload_user = models.ForeignKey('User',on_delete=models.SET_NULL,default=None,null=True)
    file_size = models.CharField(max_length=255,null=True)


class Collect(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    article = models.ForeignKey('Article',on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)
