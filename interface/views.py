from django.http import StreamingHttpResponse
import cv2
from django.shortcuts import render



def stream_video(request):
    # Открываем видеопоток с веб-камеры
    cap = cv2.VideoCapture(0)

    def generate_frames():
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # Преобразуем кадр в формат JPEG
            _, jpeg = cv2.imencode('.jpg', frame)

            # Возвращаем кадр как генератор байтовых данных
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    # Создаем объект StreamingHttpResponse и передаем генератор в качестве параметра
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


def index(request):
    return render(request, 'interface/index.html')