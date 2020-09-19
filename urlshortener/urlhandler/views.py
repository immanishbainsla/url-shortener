from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Shorturl
import random, string

# Create your views here.
@login_required(login_url='/login/')
def dashboard(request):
    usr = request.user
    urls = Shorturl.objects.filter(user = usr)
    return render(request, "dashboard.html", {'urls':urls})

def randomgen():
    val = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    return val

@login_required(login_url='/login/')
def generate(request):
    if request.method == 'POST':
        # generate
        if request.POST['original'] and request.POST['short']:
            # generate based on user input
            usr = request.user
            original = request.POST['original']
            short = request.POST['short']

            if len(short) != 6:
                messages.error(request, "length should be 6 chars or leave Empty")
                return redirect('/dashboard')

            check = Shorturl.objects.filter(short_query=short)
            if not check:
                new_url = Shorturl(
                    user = usr,
                    original_url = original,
                    short_query = short,
                )
                new_url.save()
                return redirect('/dashboard')
            else:
                messages.error(request, "Already Exists")
                return redirect('/dashboard')
        elif request.POST['original']:
            # generate randomly
            usr = request.user
            original = request.POST['original']
            generated = False
            while not generated:
                short = randomgen()
                check = Shorturl.objects.filter(short_query=short)
                if not check:
                    new_url = Shorturl(
                        user = usr,
                        original_url = original,
                        short_query = short,
                    )
                    new_url.save()
                    generated = True
                    return redirect('/dashboard')
            return redirect('/dashboard')
        else:
            # error
            messages.error(request, "Empty Fields")
            return redirect('/dashboard')
    else:
        return redirect('/dashboard')

def home(request, query=None):
    if not query or query is None:
        return render(request, "home.html", {})
    else:
        try:
            check = Shorturl.objects.get(short_query=query)
            check.visits = check.visits+1
            check.save()
            url_to_redirect = check.original_url
            return redirect(url_to_redirect)
        except Shorturl.DoesNotExist:
            return render(request, 'home.html', {'error': 'Invalid Url requested'})
