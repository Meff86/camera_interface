from django.shortcuts import render, redirect
from django.contrib.auth.models import User


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
                error_message = "Вы ввели неправильные данные."
        except User.DoesNotExist:
            # Пользователь не найден
            error_message = "Пользователь не найден."

        return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')
