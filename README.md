# 使用手册
## 编辑工具
Pycharm，也可用其它工具
## 数据库
使用mysql数据库，安装方式任意，phpstudy也可以
创建数据库，数据库名称：xtushare    用户：xtushare   密码：admin123
## 数据库迁移(注意要在manage.py所在目录下)
```
python manage.py migrate
```
## 启动
```
python manage.py runserver
```
浏览器访问：127.0.0.1:8000  即可 

## 依赖

```
django==2.0
requests
Markdown
django-mdeditor
pymysql
```
