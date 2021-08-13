'use strict';


const filialNameInput = document.getElementById('department_input_name_id');
const saveButton = document.getElementById('save-button_id');
const successModalBlock = document.querySelector('.add-staff__modal-finish');
const formData = {};

/* Event listener make enable save button if exists value in input */
filialNameInput.addEventListener('keyup', (event) => {
  formData['depart_name'] = event.target.value;

  event.target.value
    ? saveButton.removeAttribute('disabled')
    : saveButton.setAttribute('disabled', 'disabled')
});


saveButton.addEventListener('click', () => {
  const filialNameBlock = document.getElementById('filial-name_id');
  const filialID = filialNameBlock.getAttribute('org_id');
  formData['org_id'] = filialID !== null ? filialID : orgID;
  fetch(departmentCreateEndpoint, {
    method: 'POST',
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify(formData),
  })
  .then(response => {
    if (response.status === 201)
      return response.json();
    else
      throw new Error(response.statusText);
  })
  .then(responseJSON => successModalBlock.style.display = 'flex')
  .catch(error => console.log(error))
});
