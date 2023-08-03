import cv2
import time
import asyncio
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import paramiko
import os
from queue import Queue
import numpy as np

# Глобальные переменные
camera_numbers = [1, 2, 3, 4]
folder_number = 1
screenshot_counter = 1
value = None
# Добавьте словарь для хранения последних кадров с каждой камеры
last_frames = {}

def stream_video(request):
    camera = int(request.GET.get('camera', 1))

    # Открываем видеопоток с указанной камеры
    cap = cv2.VideoCapture(camera)

    # Установка разрешения видео
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

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
            # При выходе из генератора освобождаем ресурсы камеры
            cap.release()
        except Exception as e:
            # Обрабатываем другие исключения, если необходимо
            print("Error:", e)
            cap.release()

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

async def capture_frames(request):
    frame_interval = 0.35
    max_time = 22.5
    start_time = time.time()
    i = 0

    position_value = request.POST.get('front_value')
    while (time.time() - start_time) < max_time:
        i += 1

        # Ожидаем получения нового кадра из каждого видеопотока
        await asyncio.sleep(frame_interval)

        # Получаем последний доступный кадр из каждого видеопотока
        frame1 = last_frames[4]
        frame2 = last_frames[1]
        frame3 = last_frames[3]
        frame4 = last_frames[5]

        # Сохраняем кадр в папке с именем `value`
        cv2.imwrite(f'D:/digital/{value}/{value}_{position_value}_{i}_1.jpg', frame1)
        cv2.imwrite(f'D:/digital/{value}/{value}_{position_value}_{i}_2.jpg', frame2)
        cv2.imwrite(f'D:/digital/{value}/{value}_{position_value}_{i}_3.jpg', frame3)
        cv2.imwrite(f'D:/digital/{value}/{value}_{position_value}_{i}_4.jpg', frame4)

    return JsonResponse({'success': True})






@csrf_exempt
def example_view(request):
    global value
    if request.method == 'POST':
        value = request.POST.get('value')
        print(value)

        # value = ...  # Ваши действия с переменной value
        return JsonResponse({'success': True})  # Возвращаем JSON с подтверждением
    return render(request, 'interface/digital_camera.html')

@csrf_exempt
def save_screenshot(request):
    global folder_number, screenshot_counter, value

    # Открываем видеопоток с первой камеры
    camera = 1
    cap = cv2.VideoCapture(camera)

    # Установка разрешения видео
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Читаем кадр из видеопотока
    ret, frame = cap.read()

    # Освобождаем ресурсы камеры
    cap.release()

    # Если получен кадр, сохраняем его как изображение
    if ret:
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
    else:
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
    return render(request, 'interface/digital_camera.html')

