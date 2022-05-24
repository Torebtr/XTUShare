import datetime
import hashlib
import json

from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from shareplat.func import *

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


def logout(request):
    request.session.clear()
    return HttpResponseRedirect('/XTUShare/login/')


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

        if User.objects.filter(email=email).count() > 0:
            context = {
                'username': username,
                'password': password,
                'name': name,
                'email': email,
                'info': '该邮箱已被注册'
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
        return render(request, 'login.html', context=context)


def myarticle(request, page_num):
    try:
        current_user = User.objects.filter().get(id=int(request.session['user']))   # 用户验证
    except:
        return HttpResponseRedirect('/XTUShare/login/')
    if request.method == "GET":
        if current_user == "XTUShare":
            articles = Article.objects.all().order_by('-update_time')
        else:
            articles = Article.objects.filter(author=current_user).order_by('-update_time')     # 按时间降序
        page_sum = int(articles.count() / 10) + 1
        page_num = int(page_num) - 1
        if page_num < 0 or page_num >= page_sum:
            context = {
                'current_user': current_user,
                'info': '页码有误'
            }
            return render(request, 'show_info.html', context=context)
        articles = articles[page_num*10:page_num*10 + 10]
        my_articles = []

        for article in articles:
            try:
                tags = article.tags.split(',')
                if '' in tags:
                    tags.remove('')
            except Exception as e:
                tags = []
            my_articles.append(
                Article_temp(
                    article,
                    tags
                )
            )
        context = {
            'current_user': current_user,
            'my_articles': my_articles,
            'page_num': page_num + 1,
            'page_sum': page_sum,
            'pre_num': page_num,
            'next_num': page_num + 2,
        }
        return render(request, 'myarticle.html', context=context)


def create_article(request):
    try:
        current_user = User.objects.filter().get(id=int(request.session['user']))
    except:
        return HttpResponseRedirect('/XTUShare/login/')

    if request.method == "GET":
        all_classify = Classify.objects.all()
        all_tag = Tag.objects.all()
        context = {
            'current_user': current_user,
            'all_classify': all_classify,
            'all_tag': all_tag
        }
        return render(request, 'create_article.html', context=context)
    else:
        title = request.POST.get('title')
        classify = Classify.objects.get(id=int(request.POST.get('classify')))
        tags = request.POST.getlist('tag')
        content = request.POST.get('content')
        action = request.POST.get('action')
        article_type = request.POST.get('article_type')
        article_link = request.POST.get('article_link')
        if action == "save":
            Article.objects.create(
                author=current_user,
                title=title,
                classify=classify,
                tags=list2str(tags),
                content=content,
                create_time=datetime.datetime.now(),
                state=1,      # 暂存
                type=int(article_type),
                article_link=article_link,
                update_time=datetime.datetime.now()
            )
        else:
            Article.objects.create(
                author=current_user,
                title=title,
                classify=classify,
                tags=list2str(tags),
                content=content,
                create_time=datetime.datetime.now(),
                state=2,      # 发布
                type=int(article_type),
                article_link=article_link,
                update_time=datetime.datetime.now()
            )
        return HttpResponseRedirect('/XTUShare/myarticle/1/')


def delete_article(request):
    try:
        current_user = User.objects.filter().get(id=int(request.session['user']))
    except:
        return HttpResponseRedirect('/XTUShare/login/')

    if request.method == "POST":
        article_id = request.POST.get('article_id')
        try:
            article = Article.objects.get(id=article_id)
            if current_user == article.author or current_user.username == 'XTUShare':
                article.delete()
                context = {
                    'info': 'ok'
                }
            else:
                context = {
                    'info':'error'
                }
        except:
            context = {
                'info': 'error'
            }
        context = json.dumps(context)
        return JsonResponse(context, safe=False)


def go_set_classify(request):
    try:
        current_user = User.objects.filter().get(id=int(request.session['user']))
    except:
        return HttpResponseRedirect('/XTUShare/login/')

    if request.method == "POST":
        article_ids = request.POST.getlist('article_ids')
        new_articles = []
        for select_article_id in article_ids:
            article = Article.objects.get(id=int(select_article_id))
            if article.title.__len__() > 20:
                article.title = article.title[:20] + '...'
            try:
                tags = article.tags.split(',')
                if '' in tags:
                    tags.remove('')
            except:
                tags = []
            new_articles.append(
                Article_temp(
                    article,
                    tags
                )
            )

        classifys = Classify.objects.all().order_by('name')
        context = {
            'article_ids':article_ids,
            'classifys':classifys,
            'current_user':current_user,
            'new_articles':new_articles
        }
        return render(request,'set_classify.html',context=context)


def set_classify(request):
    try:
        current_user = User.objects.filter().get(id=int(request.session['user']))
    except:
        return HttpResponseRedirect('/XTUShare/login/')

    if request.method == "POST":
        article_ids = request.POST.getlist('article_ids')
        select_classify = request.POST.get('select_classify')
        classify = Classify.objects.get(id=int(select_classify))
        for article_id in article_ids:
            article = Article.objects.get(id=int(article_id))
            if article.author != current_user:
                continue
            article.classify = classify
            article.save()
        return HttpResponseRedirect('/XTUShare/myarticle/1/')


def go_set_tags(request):
    try:
        current_user = User.objects.filter().get(id=int(request.session['user']))
    except:
        return HttpResponseRedirect('/XTUShare/login/')

    if request.method == "POST":
        article_ids = request.POST.getlist('article_ids')
        new_articles = []
        for select_article_id in article_ids:
            article = Article.objects.get(id=int(select_article_id))
            if article.title.__len__() > 20:
                article.title = article.title[:20] + '...'
            try:
                tags = article.tags.split(',')
                if '' in tags:
                    tags.remove('')
            except:
                tags = []
            new_articles.append(
                Article_temp(
                    article,
                    tags
                )
            )

        tags = Tag.objects.all().order_by('name')
        context = {
            'article_ids':article_ids,
            'tags':tags,
            'current_user':current_user,
            'new_articles':new_articles
        }
        return render(request,'set_classify.html',context=context)


def set_tags(request):
    try:
        current_user = User.objects.filter().get(id=int(request.session['user']))
    except:
        return HttpResponseRedirect('/XTUShare/login/')

    if request.method == "POST":
        article_ids = request.POST.getlist('article_ids')
        select_tags = request.POST.get('select_tags')
        append_tags = ''
        for tag in select_tags:
            append_tags += tag + ','
        for article_id in article_ids:
            article = Article.objects.get(id=int(article_id))
            if article.author != current_user:
                continue
            if article.tags == None:
                article.tags = append_tags
            else:
                article.tags += append_tags
            article.save()
        return HttpResponseRedirect('/XTUShare/myarticle/1/')


def search_result(request):
    try:
        current_user = User.objects.filter().get(id=int(request.session['user']))
    except:
        return HttpResponseRedirect('/XTUShare/login/')

    keytext = request.POST.get('keytext')
    all_article = Article.objects.filter(
Q(state=3) & (Q(title__icontains=keytext) | Q(content__icontains=keytext))).order_by('-update_time')

    all_article_temps = []
    for article in all_article:
        article.content = article.content[:60] + '...'
        try:
            tags = article.tags.split(',')
            if '' in tags:
                tags.remove('')
        except:
            tags = []
        all_article_temps.append(
            Article_temp(
                article=article,
                tags=tags
            )
        )
    context = {
        'current_user': current_user,
        'all_article': all_article_temps,
        'keytext': keytext
    }

    return render(request, 'search_result.html', context=context)

def library(request):
    try:
        current_user = User.objects.filter().get(id=int(request.session['user']))
    except:
        return HttpResponseRedirect('/XTUShare/login/')

    if request.method == 'GET':
        all_articles = Article.objects.filter(state=3).order_by('-update_time')
        all_classify = Classify.objects.all().order_by('name')
        all_user = User.objects.all().order_by('name')
        all_tags = Tag.objects.all().order_by('name')

        all_article_dict = {}
        for classify in all_classify:
            all_article_dict[classify] = all_articles.filter(classify_id=classify.id)

        context = {
            'current_user': current_user,
            'all_article': all_article_dict,
            'all_classify': all_classify,
            'all_article_num': all_articles.count(),
            'all_users': all_user,
            'all_tags': all_tags,
            'show_tag_state': 1,
        }

        return render(request, 'library.html', context=context)


def search_author(request):
    try:
        current_user = User.objects.filter().get(id=int(request.session['user']))
    except:
        return HttpResponseRedirect('/XTUShare/login/')

    if request.method == 'POST':
        auther = request.POST.get('auther_name')
        try:
            user = User.objects.get(id=int(auther))
        except:
            context = {
                'current_user': current_user,
                'info': '没有该用户',
            }
            return render(request, 'show_info.html', context=context)

        all_articles = Article.objects.filter(state=3).filter(auther=user).order_by('-update_time')
        all_classify = Classify.objects.all().order_by('name')
        all_user = User.objects.all().order_by('name')
        all_tags = Tag.objects.all().order_by('name')

        all_article_dict = {}
        for classify in all_classify:
            all_article_dict[classify] = all_articles.filter(classify_id=classify.id)

        context = {
            'current_user': current_user,
            'all_article': all_article_dict,
            'all_classify': all_classify,
            'all_article_num': all_articles.count(),
            'all_users': all_user,
            'all_tags': all_tags,
            'search_user': user.id,
            'search_tag': 'null'
        }
        return render(request, 'library.html', context=context)
    else:
        context = {
            'current_user': current_user,
            'info': '不支持该请求方法',
        }
        return render(request, 'show_info.html', context=context)

def search_tag(request):
    try:
        current_user = User.objects.filter().get(id=int(request.session['user']))
    except:
        return HttpResponseRedirect('/XTUShare/login/')

    if request.method == 'POST':
        tag_name = request.POST.get('tag_name')
        try:
            tag = Tag.objects.get(id=int(tag_name))
        except:
            context = {
                'current_user': current_user,
                'info': '没有该标签',
            }
            return render(request, 'show_info.html', context=context)
        all_article = Article.objects.filter(state=3).filter(tags__contains=str(tag.id) + ',').order_by('-update_time')
        all_classify = Classify.objects.all().order_by('name')
        all_users = User.objects.all().order_by('name')
        all_tags = Tag.objects.all().order_by('name')

        all_article_dict = {}
        for classify in all_classify:
            all_article_dict[classify] = all_article.filter(classify_id=classify.id)

        context = {
            'current_user': current_user,
            'all_article': all_article_dict,
            'all_classify': all_classify,
            'all_article_num': all_article.count(),
            'all_users': all_users,
            'all_tags': all_tags,
            'search_tag': tag.id,
            'search_user': 'null'
        }
        return render(request, 'library.html', context=context)
        # return render(request, 'search_result.html', context=context)
    else:
        context = {
            'current_user': current_user,
            'info': '不支持该请求方法',
        }
        return render(request, 'show_info.html', context=context)
