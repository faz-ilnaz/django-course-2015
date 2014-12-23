from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.template import RequestContext
from django.utils.datetime_safe import datetime
from django.views.generic import FormView
from main_app.forms import UserForm, UserProfileForm, LoginForm
from main_app.models import Task, Project, Label


# returns inbox project
@login_required(login_url=reverse_lazy("sign_in"))
def index(request):
    # print(projects)
    query = Q(owner=request.user) & Q(name__iexact='inbox')

    try:
        curr_project = Project.objects.get(query)
    except Project.DoesNotExist:
        curr_project = None
    if curr_project is None:
        p = Project(name='inbox')
        p.owner = request.user
        p.save()
        curr_project = p
    # projects = Project.objects.filter(owners__in=[request.user.id])
    # print(projects)
    # print(request.user.id)
    # curr_project_id = curr_project.id
    labels = Label.objects.filter(user=request.user)

    context = {
        'labels': labels,
        # 'projects': projects,
        # 'curr_project': curr_project,
        # 'curr_project_id': curr_project_id,
        # 'tasks': Task.objects.filter(project=curr_project).order_by("-t_date")
    }
    # print(curr_project)
    return render(request, 'main_app/index.html',
                  context)


# @login_required(login_url=reverse_lazy("sign_in"))
# def certain_project(request, project_id='-1'):
#     project_id = int(project_id)
#     projects = Project.objects.filter(owners__in=[request.user])
#     if project_id == -1:
#         query = Q(name__iexact='inbox')
#     else:
#         query = Q(pk=int(project_id))
#     curr_project = Project.objects.get(query)
#
#     return render(request, 'main_app/index.html',
#                   # {"tasks": Task.objects.filter(project=project).order_by("-t_date")})
#                   # {"tasks": Task.objects.filter().order_by("-t_date")})
#                   {'projects': projects,
#                    'curr_project': curr_project,
#                    "tasks": Task.objects.filter(project=curr_project).order_by("-t_date")})


def all_projects(request):
    if request.method == 'POST':
        name = request.POST["project_name"]
        p = Project(name=name)
        p.save()
        p.owner.add(request.user)
        # p.save()
        projects = Project.objects.filter(owner=request.user)
        return render(request, 'main_app/projects.html', {'projects': projects})
    else:
        projects = Project.objects.filter(owner=request.user)
        return render(request, 'main_app/projects.html', {'projects': projects})


@login_required(login_url=reverse_lazy("sign_in"))
def process(request):
    task_desc = request.POST["task_desc"]
    project_id = request.POST["project_id"]
    task = Task(title=task_desc, t_date=datetime.now(), isDone=False)
    task.project = Project.objects.get(id=project_id)
    task.save()
    return redirect('certain_project', project_id=project_id)


def about(request):
    new_tasks_count = 0
    if request.session.has_key('ADDED_NEW_TASKS'):
        new_tasks_count = request.session['ADDED_NEW_TASKS']

    return render(request, 'main_app/about.html', {'new_tasks_count' : new_tasks_count})


@login_required(login_url=reverse_lazy("sign_in"))
def labels(request):
    if request.method == 'POST':
        title = request.POST["label_title"]
        l = Label(title=title)
        l.user = request.user
        l.save()
        # p.save()
        labels = Label.objects.filter(user=request.user)
        return render(request, 'main_app/labels.html', {'labels': labels})
    else:
        labels = Label.objects.filter(user=request.user)
        return render(request, 'main_app/labels.html', {'labels': labels})


@login_required(login_url=reverse_lazy("sign_in"))
def filters(request):
    return render(request, 'main_app/filters.html')


def no_auth(v):
    def wrapper(request, *a, **k):
        user = request.user
        if user.is_authenticated():
            return HttpResponseRedirect(reverse("index"))
        else:
            return v(request, *a, **k)

    return wrapper


# User Register View
# def user_register(request):
# if request.user.is_anonymous():
# if request.method == 'POST':
#             form = UserRegisterForm(request.POST)
#             if form.is_valid:
#                 form.save()
#                 return HttpResponse('User created succcessfully.')
#         else:
#             form = UserRegisterForm()
#         context = {}
#         context.update(csrf(request))
#         context['form'] = form
#         #Pass the context to a template
#         return render_to_response('signup.html', context)
#     else:
#         return HttpResponseRedirect('/')


# @login_required(login_url=reverse_lazy('sign_in'))
# def profile(request):
#     return render(request, 'main_app/profile.html')


@no_auth
def sign_up(request):
    context = RequestContext(request)

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()
            user_profile = profile_form.save(commit=False)
            user_profile.user = user
            p = Project(name='inbox')
            p.owner = user
            p.save()

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            user_profile.save()
            return redirect(reverse_lazy('index'))
        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
        'main_app/signup.html',
        {'user_form': user_form, 'profile_form': profile_form},
        context)


@login_required(login_url=reverse_lazy('sign_in'))
def profile(request):
    context = RequestContext(request)

    user = request.user
    profile = request.user.profile

    if request.method == 'POST':

        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        # birth_date = request.POST['birth_date']
        about_me = request.POST['about_me'].strip()

        profile.about_me = about_me
        # if birth_date:
        #     profile.birth_date = birth_date

        user.email = email
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']

        profile.save()
        return redirect(reverse_lazy('profile'))
    else:
        context['firstname'] = user.first_name
        context['lastname'] = user.last_name
        context['email'] = user.email
        # context['birth_date'] = profile.birth_date
        context['about_me'] = profile.about_me
        context['avatar'] = profile.avatar



    return render_to_response(
        'main_app/profile.html',

        context)


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy("index")
    template_name = "main_app/signin.html"

    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        if self.request.GET.has_key("next"):
            context["next"] = self.request.GET["next"]
        return context

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user:
            if user.is_active:
                login(self.request, user)
                if 'next' in self.request.GET:
                    return redirect(self.request.GET["next"])
                else:
                    return redirect(reverse_lazy('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            return redirect(reverse_lazy('sign_in'))



@login_required(login_url=reverse_lazy("sign_in"))
def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("sign_in"))