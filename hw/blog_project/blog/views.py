from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import context
from blog.models import Post
from django.db import connection


def index(request):
    posts_list = Post.objects.all().order_by("-p_date")
    paginator = Paginator(posts_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/content.html", {"posts": posts})


    # return render(request,
    # "blog/content.html",
    # {"posts": Post.objects.all().order_by("-p_date")})


def new_post(request):
    if request.POST:
        title = request.POST["title"]
        text = request.POST["text"]
        t = Post(title=title, text=text, p_date=datetime.now())
        t.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "blog/new_post.html")


def search(request):
    some_text = ''
    posts = []

    if request.GET:
        some_text = request.GET.get('text_field')
        if some_text:
            query = Q(title__contains=some_text) | Q(text__contains=some_text)
            posts_list = Post.objects.filter(query)
            paginator = Paginator(posts_list, 3)
            page = request.GET.get('page')
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
                
    queries_without_page = request.GET.copy()
    if 'page' in queries_without_page:
        del queries_without_page['page']
    query_string = queries_without_page.urlencode()

    return render(request, 'blog/search.html', {'posts': posts, 'search_text': some_text, 'query_string': query_string})