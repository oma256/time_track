'use strict';


$('.button-table__show').click((e) => {
  const id = e.currentTarget.getAttribute('id');
  const tableBlock = document.getElementById(`department_${id}`);
  const hideBtn = document.getElementById(`hide_${id}`);
  const showBtn = document.getElementById(`${id}`);
  const data = {
    depart_pk: id,
    is_hide: true,
    org_id: orgID,
  };

  fetch(filialsEndpoint, {
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
  const data = {
    depart_pk: id,
    is_hide: false,
    org_id: orgID,
  };

  fetch(filialsEndpoint, {
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
