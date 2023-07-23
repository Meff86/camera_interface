document.addEventListener("DOMContentLoaded", function() {
  // Получаем ссылку на форму
  var form = document.querySelector(".digital__process-form-photo");
  var formFront = document.querySelector(".digital__process-form-photo-front");
  var digCameraForm = document.querySelector(".digital__process-form-photo-front");
  // Получаем ссылку на кнопку
  var runButton = document.querySelector(".digital__process-run");
  var runFrontButton = document.querySelector(".digital__process-front-run");
  var runDiskButton = document.querySelector(".digital-button__record");

  runFrontButton.addEventListener("click", async function () {
  try {
    const csrfToken = getCsrfToken();

    const response = await fetch('/interface/capture_frames/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
      },
    });

    // Остальной код...
  } catch (error) {
    console.error('Произошла ошибка:', error);
  }
});
runDiskButton.addEventListener("click", async function () {
  event.preventDefault();
  try {
    const csrfToken = getCsrfToken();

    const response = await fetch('/interface/send_files/', {  // Проверьте этот путь
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
      },
    });

    if (response.ok) {
      console.log('Файлы успешно отправлены на сервер.');
    } else {
      console.error('Произошла ошибка при отправке файлов на сервер.');
    }
  } catch (error) {
    console.error('Произошла непредвиденная ошибка:', error);
  }
});




function getCsrfToken() {
  const csrfTag = document.querySelector("meta[name='csrf-token']");
  return csrfTag ? csrfTag.getAttribute("content") : '';
}



  // Добавляем обработчик клика на кнопку
  runButton.addEventListener("click", function(event) {
    event.preventDefault();

    // Изменяем стиль фона формы
    form.style.backgroundColor = "green";

    // Отображаем модальное окно и активируем чекбокс "photo"
    showModal("Сфотографируйте артикул детали", "photo");
  });

  // Функция для отображения модального окна и активации чекбокса
  function showModal(message, checkboxId) {
    var modal = document.createElement("div");
    modal.className = "modal";
    modal.innerHTML = `
      <div class="modal-content">
        <p>${message}</p>
        <button class="modal-ok-button" name="ok_button">OK</button>
      </div>
    `;
    document.body.appendChild(modal);

    var modalOkButton = modal.querySelector(".modal-ok-button");
    modalOkButton.addEventListener("click", function() {
      // Активируем чекбокс "photo"
      var checkbox = document.getElementById(checkboxId);
      checkbox.checked = true;
      console.log("Modal shown. Checkbox ID:", checkboxId);

      // Make an AJAX request to save the screenshot
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/interface/save_screenshot/');
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      var formData = new FormData();
      formData.append('current_article_number', current_article_number);
      xhr.send(formData);

      console.log("Отправленное значение current_article_number:", current_article_number);

      // Возвращаем стандартный стиль фона формы
      form.style.backgroundColor = "";

      // Удаляем модальное окно
      modal.parentNode.removeChild(modal);
    });
  }
});


function openFullscreen() {
  var elem = document.getElementById("video");
  if (elem.requestFullscreen) {
    elem.requestFullscreen().then(function() {
      elem.width = 1920;
      elem.height = 1080;
    });
  } else if (elem.mozRequestFullScreen) { // Firefox
    elem.mozRequestFullScreen().then(function() {
      elem.width = 1920;
      elem.height = 1080;
    });
  } else if (elem.webkitRequestFullscreen) { // Chrome, Safari and Opera
    elem.webkitRequestFullscreen().then(function() {
      elem.width = 1920;
      elem.height = 1080;
    });
  } else if (elem.msRequestFullscreen) { // IE/Edge
    elem.msRequestFullscreen().then(function() {
      elem.width = 1920;
      elem.height = 1080;
    });
  }
}

document.addEventListener("fullscreenchange", function() {
  var elem = document.getElementById("video");
  if (!document.fullscreenElement) {
    elem.width = 640;
    elem.height = 480;
  }
});
