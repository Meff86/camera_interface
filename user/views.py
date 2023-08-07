from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.views import logout_then_login

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('interface:digital_camera'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('interface:digital_camera'))
        else:
            messages.error(request, 'Вы ввели неправильные данные.')

    return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    return redirect('user:login')
