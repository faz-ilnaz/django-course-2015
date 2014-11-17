from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.template import RequestContext
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from main_app.forms import UserForm, UserProfileForm, LoginForm
from main_app.models import Task, Member, Project


@login_required(login_url=reverse_lazy("sign_in"))
def index(request):
    return render(request, 'main_app/index.html',
                  # {"tasks": Task.objects.filter(project=request.user.member.project_set).order_by("-t_date")})
                  {"tasks": Task.objects.filter().order_by("-t_date")})


@login_required(login_url=reverse_lazy("sign_in"))
def process(request):
    task_desc = request.POST["task_desc"]
    task = Task(title=task_desc, t_date=datetime.now(), isActive=True)
    task.save()
    print "GOT " + task.__str__()
    return HttpResponseRedirect(reverse('index'))


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
#         if request.method == 'POST':
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

            profile = profile_form.save(commit=False)
            # profile.user = user

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            profile.save()
            member = Member(user=user, profile=profile)
            member.save()
            member.project_set.create(name='inbox')
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