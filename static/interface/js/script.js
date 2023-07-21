document.addEventListener("DOMContentLoaded", function() {
  // Получаем ссылку на форму
  var form = document.querySelector(".digital__process-form-photo");

  // Получаем ссылку на кнопку
  var runButton = document.querySelector(".digital__process-run");


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
