'use strict';


(function() {
  createBeginTimeHoursItems();
  createBeginTimeMinutesItems();
  createEndTimeHoursItems();
  createEndTimeMinutesItems();
  createNonFinedTimeMinutesItems();
})();

const setEnabledButtonState = (inputsState) => {
  if (inputsState)
    saveButton.removeAttribute('disabled');
  else
    saveButton.setAttribute('disabled', 'disabled');
};

const checkInputsValExists = inputsList => {
  const inputsState = inputsList.every(currentValue => {
    return currentValue['valIsExist'] === true;
  });
  setEnabledButtonState(inputsState);
};

const saveButton = document.getElementById('save_button_id');

/* Checking for mandatory fields */
const lastNameInputBlock = {
  input: document.getElementById('input1_id'),
  errorMsg: document.getElementById('input1_error_id'),
  valIsExist: true,
};
const firstNameInputBlock = {
  input: document.getElementById('input2_id'),
  errorMsg: document.getElementById('input2_error_id'),
  valIsExist: true,
};
const middleNameInputBlock = {
  input: document.getElementById('input3_id'),
  errorMsg: document.getElementById('input3_error_id'),
  valIsExist: true,
};
const positionInputBlock = {
  input: document.getElementById('input4_id'),
  errorMsg: document.getElementById('input4_error_id'),
  valIsExist: true,
};
const phoneNumberInputBlock = {
  input: document.getElementById('phone_id'),
  errorMsg: document.getElementById('input5_error_id'),
  valIsExist: true,
};
const inputsList = [
  lastNameInputBlock, firstNameInputBlock, middleNameInputBlock,
  positionInputBlock, phoneNumberInputBlock,
];

inputsList.forEach(item => {
  item['input'].addEventListener('keyup', event => {
    if (event.target.value) {
      item['errorMsg'].style.display = 'none';
      item['valIsExist'] = true;
      checkInputsValExists(inputsList);
    } else {
      item['errorMsg'].style.display = 'block';
      item['valIsExist'] = false;
      checkInputsValExists(inputsList);
    }
  })
});

/* Checking for mandatory fields */

/*---------------------------------------------------------------*/

/* Send data to server */

const getBeginHour = () => parseInt(document.getElementById('begin-hour_id').innerText);
const getBeginMinute = () => parseInt(document.getElementById('begin-min_id').innerText);
const getEndHour = () => parseInt(document.getElementById('end-hour_id').innerText);
const getEndMinute = () => parseInt(document.getElementById('end-min_id').innerText);
const getNonFinedMin = () => parseInt(document.getElementById('non-fined-min_id').innerText);


document.getElementById('save_button_id').onclick = () => {
  const successModalMsgBlock = document.getElementById('success-modal-block_id');
  const numberExistErrorMsg = document.getElementById('number_exist_error_id');
  const data = {
    last_name: document.getElementById('input1_id').value,
    first_name: document.getElementById('input2_id').value,
    middle_name: document.getElementById('input3_id').value,
    position: document.getElementById('input4_id').value,
    phone_number: document.getElementById('phone_id').value,
    begin_hour: getBeginHour(),
    begin_min: getBeginMinute(),
    end_hour: getEndHour(),
    end_min: getEndMinute(),
    non_fined_min: getNonFinedMin(),
    org_id: orgID,
    user_org_id: userOrgID,
  };

  fetch(employeeEditEndpoint, {
    method: 'PUT',
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
    numberExistErrorMsg.style.display = 'block';
  })
};

/* Save button */

/*------------------------------------------------------------------*/

/* Remove user */

const removeButton = document.getElementById('remove_button_id');
const successRemovedBlock = document.getElementById('success-remove-modal-block_id');

removeButton.onclick = () => {
  const data = {
    user_org_id: userOrgID,
    org_pk: orgID,
  };

  fetch(employeeEditEndpoint, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-type': 'application/json, text/plain, */*',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify(data)
  })
  .then(handleErrors)
  .then(responseJSON => {
    successRemovedBlock.style.display = 'flex';
    setTimeout(() => window.location.href = responseJSON['success_url'], 2000);
  })
  .catch(err => {
    console.error(err);
  })
};

/* Remove user */
