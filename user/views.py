from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import logout_then_login

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return redirect(request.GET.get('next') or '/interface/digital_camera/')
            else:
                messages.error(request, 'Вы ввели неправильные данные.')
        except User.DoesNotExist:
            messages.error(request, 'Пользователь не найден.')

        return redirect('user:login')

    return render(request, 'user/login.html')


def logout_view(request):
    return logout_then_login(request, login_url='user:login')
