import cv2
import time
import asyncio
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import paramiko
import os
from .models import CarPart, Photo, MatchingArticle, VerifiedArticle
from queue import Queue
import numpy as np
from .forms import CarPartForm
from django.contrib.auth.decorators import user_passes_test
import boto3
from botocore.exceptions import NoCredentialsError
import shutil
from django.utils import timezone
from datetime import datetime
from .json_utils import CustomJSONEncoder
import json

AWS_S3_ACCESS_KEY_ID = 'YCAJED2HUj8DMX6N6ROlMjD4O'
AWS_S3_SECRET_ACCESS_KEY = 'YCMZKYsIcf9dQN7MC_Hoe9-8mQhZcxusZb4VeZu1'
AWS_STORAGE_BUCKET_NAME = 'meff1986'
AWS_S3_ENDPOINT_URL = 'https://storage.yandexcloud.net'


# Глобальные переменные
camera_numbers = [1, 2, 3, 4, 5, 6, 7]
folder_number = 1
screenshot_counter = 1
value = None
# Добавьте словарь для хранения последних кадров с каждой камеры
last_frames = {}
s3 = boto3.client(
    's3',
    aws_access_key_id='YCAJED2HUj8DMX6N6ROlMjD4O',
    aws_secret_access_key='YCMZKYsIcf9dQN7MC_Hoe9-8mQhZcxusZb4VeZu1',
    endpoint_url='https://storage.yandexcloud.net'

)
bucket_name = 'meff1986'

def stream_video(request):
    camera = int(request.GET.get('camera', 1))

    # Открываем видеопоток с указанной камеры
    cap = cv2.VideoCapture(camera)

    # Установка разрешения видео
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    def generate_frames():
        try:
            while True:
                ret, frame = cap.read()

                if not ret:
                    break

                # Преобразуем кадр в формат JPEG
                _, jpeg = cv2.imencode('.jpg', frame)

                # Сохраняем последний кадр в словаре
                last_frames[camera] = frame

                # Возвращаем кадр как генератор байтовых данных
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        except GeneratorExit:
            pass

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


def capture_frames(request):
    frame_interval = 0.35
    max_time = 22.5
    start_time = time.time()
    i = 0

    position_value = request.POST.get('front_value')
    current_time = datetime.now().strftime("%Y_%m_%d")
    folder_name = f"{current_time}_{value}"  # Replace 'temp_dir' with the desired temporary directory path
    folder_path = os.path.join(folder_name)
    os.makedirs(folder_path, exist_ok=True)

    while (time.time() - start_time) < max_time:
        i += 1

        # Ожидаем получения нового кадра из каждого видеопотока
        time.sleep(frame_interval)

        # Получаем последний доступный кадр из каждого видеопотока
        frame1 = last_frames[5]
        frame2 = last_frames[2]
        frame3 = last_frames[3]
        frame4 = last_frames[3]

        # Создаем экземпляр модели Photo и ассоциируем его с моделью CarParts
        car_part = CarPart.objects.get(article_number=value) if value else None


        # Создаем и сохраняем фотографии
        for frame_number, frame in enumerate([frame1, frame2, frame3, frame4], start=1):
            current_time = datetime.now().strftime("%Y_%m_%d")

            filename = f'{value}_{position_value}_{i}_{frame_number}.jpg'
            filepath = f'{current_time}_{value}/{filename}'


            # Сохраняем кадр как изображение
            cv2.imwrite(filepath, frame)
            s3_path = f"{filepath}"
            s3.upload_file(filepath, bucket_name, s3_path)

            # Проверяем, существует ли уже объект Photo с таким image_url
            existing_photo = Photo.objects.filter(image_url='https://storage.yandexcloud.net/meff1986/' + s3_path).first()
            if not existing_photo:
                # Если объекта Photo с таким image_url нет, то создаем новый объект
                photo = Photo.objects.create(car_part=car_part, image_url='https://storage.yandexcloud.net/meff1986/' + s3_path)

            # Удаляем локальный файл после успешной загрузки на S3

    shutil.rmtree(folder_path)
    return JsonResponse({'success': True})


def example_view(request):
    global value
    if request.method == 'POST':
        value = request.POST.get('value')

        if value:
            matching_car_part = CarPart.objects.filter(article_number=value).first()

            if matching_car_part:
                matching_article, created = MatchingArticle.objects.get_or_create(
                    article_number=matching_car_part.article_number)
            else:
                error_message = 'Вы ввели неправильный артикул'
                print(error_message)
                return JsonResponse({'error_message': error_message})  # Возвращаем сообщение об ошибке в AJAX-ответ

        matching_articles = MatchingArticle.objects.all()
        return render(request, 'interface/control_page.html', {'matching_articles': matching_articles})

    return render(request, 'interface/digital_camera.html')


@csrf_exempt
def save_screenshot(request):
    global folder_number, screenshot_counter, value

    # Открываем видеопоток с первой камеры
    camera = 1
    cap = cv2.VideoCapture(camera)

    # Установка разрешения видео
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)


    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    time.sleep(10)
    ret, frame = cap.read()
    if not ret:
        cap.release()  # Освобождаем ресурсы камеры
        return HttpResponse('Failed to capture a frame from camera.')



    # Если получен кадр, сохраняем его как изображение
    if ret:
        try:
            # Create a folder if it doesn't exist
            current_time = datetime.now().strftime("%Y_%m_%d")

            folder_name = f"{current_time}_{value}"  # Replace 'temp_dir' with the desired temporary directory path
            folder_path = os.path.join(folder_name)
            os.makedirs(folder_path, exist_ok=True)


            # Save the frame as an image file with a unique name, including the article number if available
            if value:
                filename = f"article_{screenshot_counter}_{value}.jpg"
            else:
                filename = f"article_{screenshot_counter}.jpg"

            filepath = os.path.join(folder_path, filename)
            cv2.imwrite(filepath, frame)
            s3_path = f"{folder_name}/{filename}"
            s3.upload_file(filepath, bucket_name, s3_path)
            # Increment the screenshot counter
            screenshot_counter += 1

            car_part = CarPart.objects.get(article_number=value) if value else None
            existing_photo = Photo.objects.filter(image_url='https://storage.yandexcloud.net/meff1986/' + s3_path).first()
            if not existing_photo:
                # Если объекта Photo с таким image_url нет, то создаем новый объект
                photo = Photo.objects.create(car_part=car_part,
                                             image_url='https://storage.yandexcloud.net/meff1986/' + s3_path)

            # If the 'OK' button is clicked in the modal dialog, create a new folder for the next screenshots
            if request.POST.get('button') == 'OK':
                folder_number += 1
                screenshot_counter = 1

        finally:
            cap.release()  # Освобождаем ресурсы камеры
            shutil.rmtree(folder_path)  # Удаляем временную папку

        # Return a response indicating success
        return HttpResponse('Screenshot saved successfully.')
    else:
        cap.release()  # Освобождаем ресурсы камеры
        return HttpResponse('Failed to capture a frame from camera 1.')



@csrf_exempt
def send_files_to_server(request):
    local_path = "D:/digital"
    server_ip = "95.163.233.68"
    server_login = "root"
    server_password = "Mrhk%3+#yuqx"
    remote_path = "/var/Foto/"

    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to server
        ssh.connect(server_ip, username=server_login, password=server_password)

        # Create remote destination folder if it does not exist
        ssh.exec_command(f"mkdir -p {remote_path}")

        for root, dirs, files in os.walk(local_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, local_path)
                remote_file_path = os.path.join(remote_path, relative_path)

                # Create remote directories if they do not exist
                ssh.exec_command(f"mkdir -p {os.path.dirname(remote_file_path)}")

                sftp = ssh.open_sftp()
                sftp.put(local_file_path, remote_file_path)
                sftp.close()

    except paramiko.AuthenticationException:
        print("Authentication error. Please check your credentials.")
        return JsonResponse({'success': False, 'error': 'Authentication error. Please check your credentials.'},
                            status=500)
    except paramiko.SSHException as ssh_exception:
        print(f"SSH error: {ssh_exception}")
        return JsonResponse({'success': False, 'error': f'SSH error: {ssh_exception}'}, status=500)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'success': False, 'error': f'Error: {e}'}, status=500)
    finally:
        ssh.close()

    return JsonResponse({'success': True})


def digital_camera(request):
    if request.user.groups.filter(name='Контролеры').exists():
        return redirect('interface:control_page')
    return render(request, 'interface/digital_camera.html')





def save_car_part(request):
    if request.method == 'POST':
        article_number = request.POST.get('modal-article')
        name = request.POST.get('modal-name')
        place = request.POST.get('modal-place')

        # Создание объекта модели и сохранение в базу данных
        new_entry = CarPart(article_number=article_number, name=name, place=place)
        new_entry.save()
        return JsonResponse({'message': 'Данные успешно сохранены'})
    else:
        return JsonResponse({'message': 'Неверный метод запроса.'}, status=400)

@csrf_protect
def control_page(request):
    if request.user.groups.filter(name='Операторы').exists():
        return redirect('interface:digital_camera')

    if request.method == 'POST':
        article_number = request.POST.get('article_number')
        try:
            matching_article = MatchingArticle.objects.get(article_number=article_number)

            # Проверяем, есть ли такой артикул уже в VerifiedArticle
            if not VerifiedArticle.objects.filter(article_number=article_number).exists():
                # Создание записи в VerifiedArticle
                VerifiedArticle.objects.create(article_number=article_number)

            return JsonResponse({'success': True})
        except MatchingArticle.DoesNotExist:
            return JsonResponse({'success': False})

    matching_articles = MatchingArticle.objects.all()
    verified_articles = VerifiedArticle.objects.values_list('article_number', flat=True)
    verified_articles_table = VerifiedArticle.objects.all()
    return render(request, 'interface/control_page.html', {'matching_articles': matching_articles, 'verified_articles': verified_articles,'verified_articles_table': verified_articles_table})

def get_photos_by_article(request):
    article_number = request.GET.get("article_number")
    photos = Photo.objects.filter(car_part__article_number=article_number).values_list("image_url", flat=True)
    return JsonResponse({"photos": list(photos)})



def get_car_parts_json(selected_date):
    print("AJAX request received with selected date:", selected_date)
    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        car_parts = CarPart.objects.filter(added_time__date=selected_date)
    else:
        car_parts = CarPart.objects.all()

    car_parts_data = [
        {'article_number': part.article_number, 'name': part.name, 'place': part.place, 'added_time': part.added_time}
        for part in car_parts
    ]

    return JsonResponse({'car_parts': car_parts_data})


def roster_page(request):
    selected_date = request.GET.get('date')
    matching_articles = MatchingArticle.objects.values_list('article_number', flat=True)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return get_car_parts_json(selected_date)
    else:
        car_parts = CarPart.objects.all()


        context = {'car_parts': car_parts, 'matching_articles': matching_articles}
        return render(request, 'interface/roster_page.html', context)


def delete_matching_article_view(request):
    if request.method == 'POST':
        selected_article = request.POST.get('article')
        try:
            matching_article = MatchingArticle.objects.get(article_number=selected_article)
            matching_article.delete()
            return JsonResponse({'success': True})
        except MatchingArticle.DoesNotExist:
            return JsonResponse({'success': False})



