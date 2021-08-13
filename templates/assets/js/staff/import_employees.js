'use strict';


const excelTemplateBtn = document.getElementById('download_template_btn_id');
const choiceFileBtn = document.getElementById('choice_template_btn_id');
const fileSelector = document.getElementById('file-selector');
const importFileBtn = document.getElementById('import_file_btn_id');
let file = null;


excelTemplateBtn.onclick = () => {
  const url = new URL(excelTemplateDownloadUrl);
  const xhttp = new XMLHttpRequest();

  xhttp.open('GET', url, true);
  xhttp.setRequestHeader('Content-Type', 'application/json');
  xhttp.responseType = 'blob';
  xhttp.send();
  xhttp.onreadystatechange = () => {
    if (xhttp.readyState === 4 && xhttp.status === 200) {
      const today = new Date();
      const a = document.createElement('a');
      a.href = window.URL.createObjectURL(xhttp.response);
      a.download = `employees_import_template_${
        today.toDateString().split(' ').join('_')
      }.xls`;
      a.style.display = 'none';

      document.body.appendChild(a);

      return a.click();
    }
  };
};


// Choice excel file from file system
choiceFileBtn.onclick = () => {
  fileSelector.addEventListener('change', (event) => {
    importFileBtn.classList.remove('disabled-import');
    file = event.target.files[0];
  });
};


// Import xls file to DB button
importFileBtn.onclick = () => {
  const xhr = new XMLHttpRequest();
  const formData = new FormData();

  formData.append('file', file);
  xhr.open('POST', importFileUrl);
  xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
  xhr.onreadystatechange = () => {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 201) {
      alert('Импорт сотрудников в базу данных прошло успешно!');
    } else if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 400) {
      alert(
        'Импорт сотрудников в базу данных прошло не удачно! ' +
        'Причина не корректные данные в форме шаблона'
      );
    }
  };

  xhr.send(formData);
};
