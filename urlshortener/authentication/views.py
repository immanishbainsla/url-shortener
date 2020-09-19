from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here
def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            # handle login
            if request.POST['email'] and request.POST['password']:
                try:
                    user = User.objects.get(email = request.POST['email'])
                    try:
                        user = auth.authenticate(username=user.username, password=request.POST['password'])
                        auth.login(request, user)
                        # messages.success(request, "login success")
                        if request.POST['next'] != "":
                            return redirect(request.POST.get('next'))
                        return redirect('/')
                    except:
                        messages.success(request, "login failed")
                        return render(request, "login.html", {'error':"Password doesn't match"})
                except User.DoesNotExist:
                    return render(request, "login.html", {'error':"User doesn't Exist"})
            else:
                return render(request, "login.html", {'error':"Email or Password is Empty"})
        else:
            return render(request, "login.html", {})
    else:
        return redirect('/dashboard')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            # handle signup
            if request.POST['password'] == request.POST['password2']:
                if request.POST['username'] and request.POST['email'] and request.POST['password']:
                    try:
                        user = User.objects.get(email = request.POST['email'])
                        return render(request, "signup.html", {'error':"user with this Email already Exists"})
                    except User.DoesNotExist:
                        User.objects.create_user(
                            username = request.POST['username'],
                            email = request.POST['email'],
                            password = request.POST['password'],
                        )
                        messages.success(request, "Signup successful, Login Here")
                        return redirect(login)
                else:
                    return render(request, "signup.html", {'error':"Username or Email is Empty"})
            else:
                return render(request, "signup.html", {'error':"Passwords don't match"})
        else:
            # it's a get request
            return render(request, "signup.html", {})
    else:
        return redirect('/dashboard')

@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect('/login')
