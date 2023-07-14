from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Поиск пользователя по имени пользователя (username)
            user = User.objects.get(username=username)
            # Проверка правильности пароля
            if user.check_password(password):
                # Вход выполнен успешно
                return redirect('home')
            else:
                # Неправильные учетные данные
                messages.error(request, 'Вы ввели неправильные данные.')
        except User.DoesNotExist:
            # Пользователь не найден
            messages.error(request, 'Пользователь не найден.')

        return redirect(reverse('user:login'))

    return render(request, 'user/login.html')
