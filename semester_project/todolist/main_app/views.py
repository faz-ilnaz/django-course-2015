from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.datetime_safe import datetime
from main_app.models import Task


def index(request):
    return render(request, 'main_app/index.html',
                  {"tasks": Task.objects.all().order_by("-t_date")})


def process(request):
    task_desc = request.POST["task_desc"]
    task = Task(title=task_desc, t_date=datetime.now(), isActive=True)
    task.save()
    print "GOT " + task.__str__()
    return HttpResponseRedirect(reverse('index'))


def about(request):
    return render(request, 'main_app/about.html')


def labels(request):
    return render(request, 'main_app/labels.html')


def filters(request):
    return render(request, 'main_app/filters.html')


def profile(request):
    return render(request, 'main_app/profile.html')
