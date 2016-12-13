from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from Web.models import DUser
# Create your views here.


def home(request):
    if request.user.is_authenticated():
        is_administer = is_admin(request.user)
        return render_to_response('home.html', locals())
    else:
        return render_to_response('index.html', locals())


def sign_up(request):
    if request.method == 'POST':
        if request.POST.get('username', '') and request.POST.get('password', '') and request.POST.get('email', ''):
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            email = request.POST.get('email', '')
            if User.objects.filter(username=username).count() == 0:
                new_user = User.objects.create_user(username=username, password=password, email=email)
                duser = DUser(user=new_user)
                if request.POST.get('phone', '') and request.POST.get('department', ''):
                    phone = request.POST.get('phone', '')
                    department = request.POST.get('department', '')
                    duser.phone = phone
                    duser.department = department
                duser.save()
            else:
                form = UserCreationForm()
                return render_to_response('signup.html', {'form': form})
        return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
        return render_to_response('signup.html', {'form': form})


@login_required
def settings(request):
    is_administer = is_admin(request.user)
    duser = request.user.duser
    username = request.user.username
    email = request.user.email
    if duser.phone:
        phone = duser.phone
    if duser.department:
        department = duser.department.encode('utf-8')
    return render_to_response('settings.html', locals())


def is_admin(user):
    try:
        user.groups.get(name='administers')
    except ObjectDoesNotExist:
        return False
    else:
        return True


def user_login(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('username', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('password', ''):
            errors.append('Enter a message.')
        if not errors:
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                redirect_url = request.GET.get('next', '')
                print(redirect_url)
                if redirect_url:
                    return HttpResponseRedirect(redirect_url)
                else:
                    return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required
def save_user_info(request):
    duser = request.user.duser
    if User.objects.filter(username=request.POST.get('username', '')).count == 0:
        if request.POST.get('username', '') and request.POST.get('email', ''):
            request.user.username = request.POST.get('username', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()
        if request.POST.get('phone', '') and request.POST.get('department', ''):
            duser.phone = request.POST.get('phone', '')
            duser.department = request.POST.get('department', '').encode('utf-8')
            duser.save()
    return HttpResponseRedirect('/settings/')


@login_required
def change_password(request):
    if request.POST.get('password', '') and request.POST.get('newpassword', ''):
        password = request.POST.get('password', '')
        new_password = request.POST.get('newpassword', '')
        if request.user.check_password(password):
            request.user.set_password(new_password)
            request.user.save()
    return HttpResponseRedirect('/settings/')


def validate_username(request):
    user = User.objects.filter(username=request.GET.get('userName',''))
    if len(user) == 0:
        message = 'yes'
    else:
        message = 'no'
    return HttpResponse(message)

