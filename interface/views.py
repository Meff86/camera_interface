import cv2
import time
import asyncio
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import os

# Глобальные переменные
last_frame = None
folder_number = 1
screenshot_counter = 1
value = None

# Функция для захвата кадров

# async def capture_frames():
#     # Создание объекта VideoCapture для захвата видео с веб-камеры
#     video_capture = cv2.VideoCapture(1)  # Используем индекс веб-камеры по умолчанию (например, 0 для первой веб-камеры)
#
#     # Установка разрешения видео
#     video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#     video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
#
#     frame_interval = 0.1
#     max_time = 22.5
#     start_time = time.time()
#     i = 0
#
#     while (time.time() - start_time) < max_time:
#         i += 1
#
#         ret, frame = video_capture.read()
#
#         if not ret:
#             continue
#
#         color_file_path = f'D:/interface/color_frame_{i}.jpg'
#         cv2.imwrite(color_file_path, frame)
#
#         # Обновление последнего кадра
#         global last_frame
#         last_frame = frame
#
#         # Задержка для получения желаемого интервала кадров
#         await asyncio.sleep(frame_interval)
#
#     video_capture.release()

async def capture_frames(request):
    frame_interval = 0.1
    max_time = 22.5
    start_time = time.time()
    i = 0

    while (time.time() - start_time) < max_time:
        i += 1

        # Ожидаем получения нового кадра из генератора
        await asyncio.sleep(frame_interval)

        # Получаем последний доступный кадр из глобальной переменной
        frame = last_frame
        next_value = value

        if frame is None:
            continue

        color_file_path = f'D:/digital/{next_value}/{next_value}_{i}.jpg'
        cv2.imwrite(color_file_path, frame)

    return JsonResponse({'success': True})

@csrf_exempt
def capture_frames_view(request):
    if request.method == 'POST':
        # Вызов функции для захвата кадров с веб-камеры через асинхронный вызов
        loop = asyncio.get_event_loop()
        loop.run_until_complete(capture_frames(request))

        # Возврат ответа для подтверждения успешного выполнения запроса
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Метод должен быть POST.'}, status=400)
def stream_video(request):
    # Открываем видеопоток с веб-камеры
    cap = cv2.VideoCapture(1)

    # Установка разрешения видео
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def generate_frames():
        global last_frame
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # Обновляем последний кадр
            last_frame = frame

            # Преобразуем кадр в формат JPEG
            _, jpeg = cv2.imencode('.jpg', frame)

            # Возвращаем кадр как генератор байтовых данных
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

@csrf_exempt
def example_view(request):
    global value
    if request.method == 'POST':
        value = request.POST.get('value')
        print(value)
        # Здесь вы можете сохранить значение в переменную или делать с ним, что вам нужно
        # Например, сохранить в переменную в вашей view или в базу данных
        # value = ...  # Ваши действия с переменной value
        return JsonResponse({'success': True})  # Возвращаем JSON с подтверждением
    return render(request, 'interface/digital_camera.html')

@csrf_exempt
def save_screenshot(request):
    global last_frame, folder_number, screenshot_counter, value


    # Get the last frame of the video stream
    frame = last_frame

    # Create a folder if it doesn't exist
    folder_name = f"{value}"
    temp_dir = "D:/digital"  # Replace 'temp_dir' with the desired temporary directory path
    folder_path = os.path.join(temp_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Save the frame as an image file with a unique name, including the article number if available
    if value:
        filename = f"article_{screenshot_counter}_{value}.jpg"
    else:
        filename = f"article_{screenshot_counter}.jpg"

    filepath = os.path.join(folder_path, filename)
    cv2.imwrite(filepath, frame)

    # Increment the screenshot counter
    screenshot_counter += 1

    # If the 'OK' button is clicked in the modal dialog, create a new folder for the next screenshots
    if request.POST.get('button') == 'OK':
        folder_number += 1
        screenshot_counter = 1

    # Return a response indicating success
    return HttpResponse('Screenshot saved successfully.')




def digital_camera(request):
    return render(request, 'interface/digital_camera.html')

