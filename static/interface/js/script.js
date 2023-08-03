document.addEventListener("DOMContentLoaded", function() {
  // Получаем ссылку на форму
  var form = document.querySelector(".digital__process-form-photo");
  var formFront = document.querySelector(".digital__process-form-photo-front");
  var digCameraForm = document.querySelector(".digital__process-form-photo-front");
  // Получаем ссылку на кнопку

  var runDiskButton = document.querySelector(".digital-button__record");


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



function openFullscreen(videoId) {
  var elem = document.getElementById(videoId);
  if (elem.requestFullscreen) {
    elem.requestFullscreen().then(function() {
      elem.width = window.screen.width;
      elem.height = window.screen.height;
    });
  } else if (elem.mozRequestFullScreen) { // Firefox
    elem.mozRequestFullScreen().then(function() {
      elem.width = window.screen.width;
      elem.height = window.screen.height;
    });
  } else if (elem.webkitRequestFullscreen) { // Chrome, Safari и Opera
    elem.webkitRequestFullscreen().then(function() {
      elem.width = window.screen.width;
      elem.height = window.screen.height;
    });
  } else if (elem.msRequestFullscreen) { // IE/Edge
    elem.msRequestFullscreen().then(function() {
      elem.width = window.screen.width;
      elem.height = window.screen.height;
    });
  }
}

document.addEventListener("fullscreenchange", function() {
  var elem = document.fullscreenElement;
  if (!elem) {
    // Выход из полноэкранного режима, установите исходные значения размеров
    var videoElements = document.querySelectorAll(".digital_video-wrapper img");
    videoElements.forEach(function(video) {
      video.width = 320;
      video.height = 240;
    });
    var fullscreenIcons = document.querySelectorAll(".digital_video-wrapper a");
    fullscreenIcons.forEach(function(icon) {
      icon.firstChild.width = 40;
      icon.firstChild.height = 40;
    });
  }
});



function switchToNextForm(event) {
  event.preventDefault();
  const currentForm = document.querySelector('.current-point');
  if (currentForm.classList.contains('digital__process-form-photo')) {
    currentForm.classList.remove('current-point');
    const nextForm = document.querySelector('.digital__process-form-photo-front');
    nextForm.classList.add('current-point');
  } else if (currentForm.classList.contains('digital__process-form-photo-front')) {
    currentForm.classList.remove('current-point');
    const nextForm = document.querySelector('.digital__process-form-rear');
    nextForm.classList.add('current-point');
  } else if (currentForm.classList.contains('digital__process-form-rear')) {
    currentForm.classList.remove('current-point');
    const nextForm = document.querySelector('.digital__process-form-photo-other');
    nextForm.classList.add('current-point');
  } else if (currentForm.classList.contains('digital__process-form-photo-other')) {
    // Do something else if needed
  }
}


