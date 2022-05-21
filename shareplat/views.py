import datetime
import hashlib

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
import markdown

from shareplat.models import User, Update_log, Article


def page_main(request):
    try:
        current_user = User.objects.filter().get(id=int(request.session['user']))
    except:
        current_user = None
    if request.method == "GET":
        last_update_logs = Update_log.objects.all().order_by('-create_time')[:5]
        update_logs = []
        for last_update_log in last_update_logs:
            last_update_log.content = markdown.markdown(last_update_log.content.replace('<','&lt;').replace('>','&gt;'), extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ])
            update_logs.append(last_update_log)
        all_article = Article.objects.filter(state=3)
        new_top10_articles = all_article.order_by('-create_time')[:10]       # 最新文章列表
        read_max_articles = all_article.order_by('-read_num')[:10]           # 阅读排行榜
        for new_top10_article in new_top10_articles:
            if new_top10_article.title.__len__() > 20:
                new_top10_article.title = new_top10_article.title[:20] + '...'

        for read_max_article in read_max_articles:
            if read_max_article.title.__len__() > 20:
                read_max_article.title = read_max_article.title[:20] + '...'

        all_author = User.objects.all()
        for author in all_author:
            author.article_num = Article.objects.filter(state=3).filter(author=author).count()
            author.save()
        top10_authors = User.objects.all().order_by('-article_num')[:10]       # 作者排行榜
        context = {
            'current_user':current_user,      # 鉴权
            # 'last_update_logs':update_logs,
            'new_top10_articles':new_top10_articles,
            'read_max_articles':read_max_articles,
            'top10_authors':top10_authors,
        }
        return render(request,'main.html',context=context)


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        m = hashlib.md5(password.encode())       # 创建对象
        encry_password = m.hexdigest()           # 密码md5加密
        try:
            user = User.objects.get(username=username)
            if user.password == encry_password:
                request.session['user'] = user.id
                user.save()
                request.session.set_expiry(36000)
                return HttpResponseRedirect('/XTUShare/main/')

            else:
                user.login_fail += 1
                user.save()
                context = {
                    'info':'账号或密码错误'
                }
                return render(request,'login.html',context=context)
        except:
            context = {
                'info': '账号或密码错误'
            }
            return render(request, 'login.html', context=context)


def register(request):
    if request.method == "GET":
        return render(request,'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')

        m = hashlib.md5(password.encode())
        encry_password = m.hexdigest()

        if User.objects.filter(username=username).count() > 0:
            context = {
                'username': username,
                'password': password,
                'name': name,
                'email': email,
                'info': '该用户名已被注册'
            }
            return render(request, 'register.html', context=context)
        user = User.objects.create(
            username=username,
            password=encry_password,
            email=email,
            name=name,
            create_time=datetime.datetime.now()
        )
        user.save()
        context ={
            'info': '注册成功'
        }
        return render(request, 'register.html', context=context)
