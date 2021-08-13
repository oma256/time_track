'use strict';

const searchInput = document.getElementById('search-input_id');
const saveButton = document.getElementById('save-button_id');
const searchResultBlock = document.getElementById('search-result_id');
const searchErrorMsg = document.getElementById('search-error-msg_id');
const inputs = searchResultBlock.getElementsByTagName('input');
const modalCancelButton = document.querySelector('.modal-cancel');


$('.button-table__show').click((e) => {
  const id = e.currentTarget.getAttribute('id');
  const tableBlock = document.getElementById(`department_${id}`);
  const hideBtn = document.getElementById(`hide_${id}`);
  const showBtn = document.getElementById(`${id}`);
  const data = {depart_pk: id, is_hide: true};

  fetch(filialDetailEndpoint, {
    method: 'POST',
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(data)
  })
  .then(handleErrors)
  .then(responseJSON => {
    showBtn.style.display = 'none';
    hideBtn.style.display = 'block';
    tableBlock.innerHTML = responseJSON['html']
  })
  .catch(error => console.log(error))
});

$('.button-table__hide').click((e) => {
  const button_text_id = e.currentTarget.getAttribute('id');
  const id = button_text_id.split('_')[1];
  const hideBtn = document.getElementById(`hide_${id}`);
  const showBtn = document.getElementById(`${id}`);
  const tableBlock = document.getElementById(`department_${id}`);
  const data = {depart_pk: id, is_hide: false};

  fetch(filialDetailEndpoint, {
    method: 'POST',
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(data)
  })
  .then(handleErrors)
  .then(responseJSON => {
    showBtn.style.display = 'block';
    hideBtn.style.display = 'none';
    tableBlock.innerHTML = responseJSON['html']
  })
  .catch(error => console.log(error))
});


modalCancelButton.addEventListener('click', () => {
  const checkedItem = getUserCheckedInput(inputs);

  checkedItem
    ? checkedItem.checked = false
    : checkedItem.checked
});


searchInput.addEventListener('keyup', (event) => {
  const url = new URL(filialAddAdminEndpoint);
  const params = {name: event.target.value};

  Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

  setTimeout(() => {
    if (params.name) {
      fetch(url, {
        method: 'GET',
        headers: {'Content-Type': 'application/json'},
      })
      .then(response => {
        if (response.status === 200)
          return response.json();
        else
          throw response.statusText
      })
      .then(responseJSON => searchResultBlock.innerHTML = responseJSON['html'])
      .catch(error => console.log(error))
    }
  }, 1000)
});


saveButton.addEventListener('click', () => {
  let data = {};

  const checkedItem = getUserCheckedInput(inputs);

  if (!checkedItem) {
    searchErrorMsg.style.display = 'block';
    return;
  }

  data['user_id'] = parseInt(checkedItem.getAttribute('user_id'));
  data['filial_id'] = parseInt(filialID);

  fetch(filialAddAdminEndpoint, {
    method: 'POST',
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(data),
  })
  .then(response => {
    if (response.status === 200)
      return response.json();
    else
      throw response.statusText;
  })
  .then(responseJSON => window.location.reload(true))
  .catch(error => console.log(error))
});


const getUserCheckedInput = (inputs) => {
  for (let i = 0; i < inputs.length; i++) {
    if (inputs[i].checked) {
      return inputs[i];
    }
  }
};
