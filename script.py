import cv2

# Создаем объект VideoCapture для доступа к веб-камере
cap = cv2.VideoCapture(0)

# Проверяем, открыта ли веб-камера
if not cap.isOpened():
    print("Не удалось открыть веб-камеру")
    exit()

# Читаем кадры с веб-камеры до тех пор, пока пользователь не нажмет 'q'
while True:
    # Захватываем кадр с веб-камеры
    ret, frame = cap.read()

    # Если кадр успешно захвачен
    if ret:
        # Отображаем кадр в окне
        cv2.imshow('Web Camera', frame)

    # Проверяем, была ли нажата клавиша 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()
