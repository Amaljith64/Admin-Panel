from django.shortcuts import render, redirect

from account.decorator import admin_only
from . models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.decorators.cache import cache_control
from .decorator import *
from django.db.models import Q

# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if 'username' in request.session:
        return redirect(home)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['username'] = username
            messages.success(request, "You have been succesfully Logged in")
            return redirect('/')
        else:
            messages.info(request, 'invalid details')
            return redirect('login')

    else:
        return render(request, "login.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if 'username' in request.session:
        return redirect(home)
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email taken")
                return redirect('register')

            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)

                user.save()
                print("user created")
        else:
            messages.info(request, "Password Not match")
            return redirect('register')
        return redirect('/')
    else:
        return render(request, 'signup.html')


@admin_only
def registeruser(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username taken")
                return redirect('registeruser')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email taken")
                return redirect('registeruser')

            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print("user created")
        else:
            messages.info(request, "Password Not match")
            return redirect('registeruser')
        return redirect('/')
    else:
        return render(request, 'registeruser.html')


@admin_only
def registeradmin(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username taken")
                return redirect('registeradmin')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email taken")
                return redirect('registeradmin')

            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.is_superuser = True
                user.save()
                print("user created")
        else:
            
            messages.info(request, "Password Not match")
            return redirect('registeradmin')
        return redirect('/')
    else:
        return render(request, 'registeradmin.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if 'username' in request.session:
        return render(request, 'home.html')
    return redirect(login)


@admin_only
def admin(request):
    if 'search' in request.POST:
        search = request.POST['search']
        searchwith = Q(Q(username__icontains=search)
                       | Q(email__icontains=search))
        mydata = User.objects.filter(searchwith)
    else:
        mydata = User.objects.all()

    return render(request, 'admin.html', {'datas': mydata})


@admin_only
def update(request, id):
    updata = User.objects.get(id=id)

    if request.method == 'POST':
        name = request.POST['username']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        if name == "":
            messages.error(request, "Field is Empty")
            redirect(admin)
        elif email == "":
            messages.error(request, "Email is Empty")
            redirect(admin)
        elif User.objects.exclude(id=id).filter(username=name):
            messages.error(request, "Username Exists")
            redirect(admin)
        elif User.objects.exclude(id=id).filter(email=email):
            messages.error(request, "Email Exists")
            redirect(admin)
        else:
            updata.username = name
            updata.first_name = firstname
            updata.last_name = lastname
            updata.email = email
            updata.save()
            return redirect(admin)
    return render(request, 'update.html', {'updatas': updata})


def delete(request, id):
    mydata = User.objects.get(id=id)
    mydata.delete()
    return redirect(admin)
