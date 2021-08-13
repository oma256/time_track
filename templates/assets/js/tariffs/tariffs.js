'use strict';


const feedbackBtn = document.getElementById('feedback-btn_id');
const feedbackInput = document.getElementById('feedback-input-id');

feedbackBtn.onclick = () => {
  const phoneCode = feedbackInput.parentElement.children[1].innerText;
  const cleanPhone = unMaskedPhoneValue(feedbackInput.value);
  const data = {phone: `${phoneCode}${cleanPhone}`};

  fetch(feedbackCreateUrl, {
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
    window.location.reload(true);
  })
  .catch(error => console.log(error))
};

feedbackInput.onkeyup = (event) => {
  let value = event.currentTarget.value;
  if (feedbackPhoneInputUnMasked(value).length > 8) {
    feedbackBtn.removeAttribute('disabled');
    feedbackBtn.style.background = '#6A4B93';
  } else {
    feedbackBtn.setAttribute('disabled', 'disabled');
    feedbackBtn.style.background = '#A5ADBC';
  }
};


const currentTariffPayBtn = document.getElementById('create-payment_id');

currentTariffPayBtn.onclick = (event) => {
  const data = {
    tariff_pkg_id: parseInt(event.target.getAttribute('tariff_pkg_id')),
    org_id: parseInt(event.target.getAttribute('org_id')),
  };

  fetch(createPaymentUrl, {
    method: 'POST',
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify(data),
  })
  .then(response => response.json())
  .then(responseJSON => {
    window.location.replace(responseJSON['paybox_payment_url']);
  })
  .catch(error => console.error('error:', error))
};