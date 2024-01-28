#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import datetime
import random
from contextlib import closing

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse

from core.models import User


def sign_in(requests):
    if not requests.user.is_anonymous:
        return redirect("home")

    if requests.POST:
        data = requests.POST
        user = User.objects.filter(username=data['username']).first()
        if not user:
            return render(requests, 'pages/auth/login.html', {"error": "username xato"})

        if not user.check_password(data['pass']):
            return render(requests, 'pages/auth/login2.html', {"error": "Parol xato"})

        if not user.is_active:
            return render(requests, 'pages/auth/login2.html', {"error": "Profil active emas "})
        login(requests, user)
        requests.session['show_alert'] = ' '
        return redirect('home')
    return render(requests, 'pages/auth/login2.html')


def sign_up(requests):
    if not requests.user.is_anonymous:
        return redirect("home")

    if requests.POST:
        data = requests.POST
        user = User.objects.filter(username=data['username']).first()
        if user:
            return render(requests, 'pages/auth/regis2.html', {"error": "Bunday foydalanuvchi mavjud"})

        if data['pass'] != data['re-pass']:
            return render(requests, 'pages/auth/regis2.html', {"error": "Parollar mos kelmadi"})

        user = User.objects.create_user(data['username'], data['pass'])

        login(requests, user)
        authenticate(requests)
        requests.session['show_alert'] = ' '
        return redirect('home')
    return render(requests, 'pages/auth/regis2.html')


def hide_alert(request):
    try:
        del request.session['show_alert']
    except:
        pass
    return HttpResponse('ok')


@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect("login")


@login_required(login_url='login')
def change_password(request, user_id):
    if request.user.is_anonymous:
        return redirect('login')
    root = 0
    if request.POST and request.user.ut == 1 or request.user.ut == 3:
        root = User.objects.filter(pk=user_id).first()
        if root and root.ut != 1:
            root.set_password(request.POST.get("password"))
            root.save()
        if root == request.user:
            request.user.set_password(request.POST.get("password"))
            request.user.save()

    return redirect('user', type=3 if not root else root.ut)
