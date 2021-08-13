'use strict';


(function() {
  createBeginTimeHoursItems();
  createBeginTimeMinutesItems();
  createEndTimeHoursItems();
  createEndTimeMinutesItems();
  createNonFinedTimeMinutesItems();
})();

/* Checking for mandatory fields */
const filialsListBlock = document.querySelector('#filial_list_id');
const lastNameInput = document.getElementById('input1_id');
const input1ErrorMsg = document.getElementById('input1_error_id');
let input1ValIsExist = false;

const firstNameInput = document.getElementById('input2_id');
const input2ErrorMsg = document.getElementById('input2_error_id');
let input2ValIsExist = false;

const positionInput = document.getElementById('input4_id');
const input4ErrorMsg = document.getElementById('input4_error_id');
let input4ValIsExist = false;

const phoneNumberInput = document.getElementById('phone');
const input5ErrorMsg = document.getElementById('input5_error_id');
let input5ValIsExist = false;

const saveButton = document.getElementById('save_button_id');

const setEnabledButtonState = () => {
  saveButton.removeAttribute('disabled');
};

const setDisabledButtonState = () => {
  saveButton.setAttribute('disabled', 'disabled');
};

lastNameInput.addEventListener('keyup', (event) => {
  if (event.target.value) {
    input1ErrorMsg.style.display = 'none';
    input1ValIsExist = true;
    checkInputsValExists();
  } else {
    input1ErrorMsg.style.display = 'block';
    input1ValIsExist = false;
    checkInputsValExists();
  }
});

firstNameInput.addEventListener('keyup', (event) => {
  if (event.target.value) {
    input2ErrorMsg.style.display = 'none';
    input2ValIsExist = true;
    checkInputsValExists();
  } else {
    input2ErrorMsg.style.display = 'block';
    input2ValIsExist = false;
    checkInputsValExists();
  }
});

positionInput.addEventListener('keyup', (event) => {
  if (event.target.value) {
    input4ErrorMsg.style.display = 'none';
    input4ValIsExist = true;
    checkInputsValExists();
  } else {
    input4ErrorMsg.style.display = 'block';
    input4ValIsExist = false;
    checkInputsValExists();
  }
});

phoneNumberInput.addEventListener('keyup', (event) => {
  if (unMaskedPhoneValue(event.target.value)) {
    input5ErrorMsg.style.display = 'none';
    input5ValIsExist = true;
    checkInputsValExists();
  } else {
    input5ErrorMsg.style.display = 'block';
    input5ValIsExist = false;
    checkInputsValExists();
  }
});

const checkInputsValExists = () => {
  if (input1ValIsExist && input2ValIsExist && input4ValIsExist && input5ValIsExist) {
    setEnabledButtonState();
  } else {
    setDisabledButtonState();
  }
};
/* Checking for mandatory fields */

/*---------------------------------------------------------------*/

/* Get departments list by filial id */
const departmentListBlock = document.querySelector('#departments_block_id');

for (let filial of filialsListBlock.children) {
  const data = {filial_id: filial.id};

  filial.onclick = () => {
    fetch(departmentsByFilialEndpoint, {
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
        throw response.statusText
    })
    .then(responseJSON => {
      departmentListBlock.innerHTML = responseJSON['html'];
      selectContent();
    })
    .catch(error => console.log(error))
  }
}
/* Get departments list by filial id */

/*------------------------------------------------------------------*/

/* Send data to server */

const getBeginHour = () => parseInt(document.getElementById('begin-hour_id').innerText);
const getBeginMinute = () => parseInt(document.getElementById('begin-min_id').innerText);
const getEndHour = () => parseInt(document.getElementById('end-hour_id').innerText);
const getEndMinute = () => parseInt(document.getElementById('end-min_id').innerText);
const getNonFinedMin = () => parseInt(document.getElementById('non-fined-min_id').innerText);

saveButton.onclick = () => {
  const successModalMsgBlock = document.getElementById('success-modal-block_id');
  const filialNameBlock = document.getElementById('filial-name_id');
  const departmentNameBlock = document.getElementById('department-name_id');
  const data = {
    last_name: document.getElementById('input1_id').value,
    first_name: document.getElementById('input2_id').value,
    middle_name: document.getElementById('input3_id').value,
    position: document.getElementById('input4_id').value,
    phone_number: document.getElementById('phone').value,
    org_id: orgID,
    filial_id: filialNameBlock.getAttribute('org_id'),
    depart_id: departmentNameBlock.getAttribute('org_id'),
    begin_hour: getBeginHour(),
    begin_min: getBeginMinute(),
    end_hour: getEndHour(),
    end_min: getEndMinute(),
    non_fined_min: getNonFinedMin(),
  };

  fetch(employeeCreateEndpoint, {
    method: 'POST',
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify(data),
  })
  .then(handleErrors)
  .then(responseJSON => {
    successModalMsgBlock.style.display = 'flex';
  })
  .catch(error => {
    console.error(error.statusText);
  })
};

/* Save button */
