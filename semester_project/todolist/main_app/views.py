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
from main_app.models import Task, Project


# returns inbox project
@login_required(login_url=reverse_lazy("sign_in"))
def index(request):
    projects = Project.objects.filter(owners__in=[request.user])
    # print(projects)
    query = Q(owners__in=[request.user]) & Q(name__iexact='inbox')

    curr_project = Project.objects.get(query)
    curr_project_id = curr_project.id
    context = {'projects': projects,
               'curr_project': curr_project,
               'curr_project_id': curr_project_id,
               'tasks': Task.objects.filter(project=curr_project).order_by("-t_date")
               }
    # print(curr_project)
    return render(request, 'main_app/index.html',
                  context)


@login_required(login_url=reverse_lazy("sign_in"))
def certain_project(request, project_id='-1'):
    project_id = int(project_id)
    projects = Project.objects.filter(owners__in=[request.user])
    if project_id == -1:
        query = Q(name__iexact='inbox')
    else:
        query = Q(pk=int(project_id))
    curr_project = Project.objects.get(query)

    return render(request, 'main_app/index.html',
                  # {"tasks": Task.objects.filter(project=project).order_by("-t_date")})
                  # {"tasks": Task.objects.filter().order_by("-t_date")})
                  {'projects': projects,
                   'curr_project': curr_project,
                   "tasks": Task.objects.filter(project=curr_project).order_by("-t_date")})


def all_projects(request):
    if request.method == 'POST':
        name = request.POST["project_name"]
        p = Project(name=name)
        p.save()
        p.owners.add(request.user)
        # p.save()
        projects = Project.objects.filter(owners__in=[request.user])
        return render(request, 'main_app/projects.html', {'projects': projects})
    else:
        projects = Project.objects.filter(owners__in=[request.user])
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
    return render(request, 'main_app/about.html')


@login_required(login_url=reverse_lazy("sign_in"))
def labels(request):
    return render(request, 'main_app/labels.html')


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


@login_required(login_url=reverse_lazy('sign_in'))
def profile(request):
    return render(request, 'main_app/profile.html')


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
            p.save()
            p.owners.add(user)

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


# @no_auth
# def sign_in(request):
#     # Like before, obtain the context for the user's request.
#     # context = RequestContext(request)
#     # If the request is a HTTP POST, try to pull out the relevant information.
#     if request.method == 'POST':
#         f = LoginForm(request.POST)
#         if f.is_valid():
#             # Gather the username and password provided by the user.
#             # This information is obtained from the login form.
#             # username = request.POST['username']
#             # password = request.POST['password']
#
#             user = authenticate(
#                 username=f.cleaned_data["username"],
#                 password=f.cleaned_data["password"]
#             )
#
#             # Use Django's machinery to attempt to see if the username/password
#             # combination is valid - a User object is returned if it is.
#             # user = authenticate(username=username, password=password)
#
#             # If we have a User object, the details are correct.
#             # If None (Python's way of representing the absence of a value), no user
#             # with matching credentials was found.
#             if user:
#                 # Is the account active? It could have been disabled.
#                 if user.is_active:
#                     # If the account is valid and active, we can log the user in.
#                     # We'll send the user back to the homepage.
#                     login(request, user)
#                     if request.GET.has_key("next"):
#                         return HttpResponseRedirect(request.GET["next"])
#                     else:
#                         return HttpResponseRedirect(reverse('index'))
#                 else:
#                     # An inactive account was used - no logging in!
#                     return HttpResponse("Your Rango account is disabled.")
#             else:
#                 # Bad login details were provided. So we can't log the user in.
#                 print "Invalid login details: {0}, {1}".format(username, password)
#                 # return HttpResponse("Invalid login details supplied.")
#                 return HttpResponseRedirect(reverse('sign_in'))
#
#     # The request is not a HTTP POST, so display the login form.
#     # This scenario would most likely be a HTTP GET.
#     else:
#         # No context variables to pass to the template system, hence the
#         # blank dictionary object...
#         f = LoginForm()
#         context = {"f": f}
#         if request.GET.has_key("next"):
#             context["next"] = request.GET["next"]
#         return render(request, "main_app/signin.html", context)
#         # return render_to_response('main_app/signin.html', {}, context)


@login_required(login_url=reverse_lazy("sign_in"))
def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("sign_in"))