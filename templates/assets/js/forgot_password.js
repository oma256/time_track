'use strict';


window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier('phone', {
    'size': 'invisible',
    'callback': function (response) {
        // reCAPTCHA solved, allow signInWithPhoneNumber.
      onSignInSubmit();
    }
});

const sendPhoneBtn = document.getElementById('send-button');
const codeConfirmBtn = document.getElementById('confirm_button_id');
const sendPhoneFormBlock = document.getElementById('send_phone_block_id');
const confirmCodeFormBlock = document.getElementById('confirm_code_block_id');
const resivedPhone = document.getElementById('resived_phone_id');
const changePasswordFormBlock = $('#change_password_block_id');
const codeValidErrBlock = document.getElementById('code-valid-error');
const codeRequiredErrBlock = document.getElementById('code-required-error');
const successModalBlock = document.getElementById('success_modal_block_id');
const phoneNumberInput = document.getElementById('phone_phone_id');
const sendAgainBtn = document.getElementById('send_again_btn');

function unMaskedPhoneValue(phone) {
    return phone.replace('(', '').replace(')', '').replace(/-/g, '').replace(/\s/g, '')
}

function getPhoneNumberFromUserInput() {
    return $('input[name="phone"]').val();
}

function getVerificationCode() {
    return $('input[name="code"]').val();
}

sendPhoneBtn.onclick = () => {
  window.phoneNumber = unMaskedPhoneValue(getPhoneNumberFromUserInput());
  window.maskedPhoneNumber = getPhoneNumberFromUserInput();
  const appVerifier = window.recaptchaVerifier;

  preloadStart();

  firebase.auth().signInWithPhoneNumber(window.phoneNumber, appVerifier)
  .then(confirmationResult => {
    window.confirmationResult = confirmationResult;
    sendPhoneFormBlock.classList.remove('show');
    confirmCodeFormBlock.classList.add('show');
    resivedPhone.innerText = window.maskedPhoneNumber;
    preloaderEnd();
    startTimer();
  })
  .catch(error => {
    preloaderEnd();
    console.log('confirmation result error');
  })
};

codeConfirmBtn.onclick = () => {
  const code = getVerificationCode();

  if (code) {
    window.confirmationResult.confirm(code)
    .then(result => {
      preloadStart();
      firebase.auth().currentUser.getIdToken(true)
      .then(idToken => {
        phoneNumberInput.value = window.phoneNumber;
        confirmCodeFormBlock.classList.remove('show');
        changePasswordFormBlock.addClass('show');
        preloaderEnd();
      })
      .catch(error => console.error('error:', error))
    })
    .catch(error => {
      codeValidErrBlock.style.display = 'block';
      codeRequiredErrBlock.style.display = 'none';
    })
  } else {
    codeValidErrBlock.style.display = 'none';
    codeRequiredErrBlock.style.display = 'block';
  }
};

$(document).on("click", '#change_password_btn_id', function (e) {
  event.preventDefault();

  $.ajax({
      url: changePasswordUrl,
      method: 'POST',
      data: $('#change_pass_form').serialize(),
      success: (response) => {
        changePasswordFormBlock.removeClass('show');
        successModalBlock.classList.add('show');
      },
      error: (response) => {
        changePasswordFormBlock.html(response['responseJSON']['html']);
      }
  });
});

sendAgainBtn.onclick = () => {
  const appVerifier = window.recaptchaVerifier;

  preloadStart();

  firebase.auth().signInWithPhoneNumber(window.phoneNumber, appVerifier)
  .then(confirmationResult => {
    window.confirmationResult = confirmationResult;
    sendPhoneFormBlock.classList.remove('show');
    confirmCodeFormBlock.classList.add('show');
    resivedPhone.innerText = window.maskedPhoneNumber;
    preloaderEnd();
    startTimer();
  })
  .catch(error => {
    preloaderEnd();
    console.log('confirmation result error');
  })
};
