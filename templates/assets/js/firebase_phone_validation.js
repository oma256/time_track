'use strict';

const phoneInputBlock = $('#phone-validation-block');
const codeValidationBlock = $('#code-validation-block');
const registrationBlock = $('#registation-block');
const backgroundForm = $('#body-register-container_id');
const sendButton = document.getElementById('send-button');
const confirmButton = document.getElementById('confirm-button');
const registrationButton = document.getElementById('registration-button');
const phoneValidErrBlock = document.getElementById('phone-valid-error');
const codeValidErrBlock = document.getElementById('code-valid-error');


window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier('phone', {
    'size': 'invisible',
    'callback': function (response) {
        // reCAPTCHA solved, allow signInWithPhoneNumber.
      onSignInSubmit();
    }
});


$(document).ready(function() {
      $('form').keydown(function(event){
        if(event.keyCode == 13) {
            event.preventDefault();
            $('.send-form-data').trigger('click');

            return false;
        }
   });
});

sendButton.onclick = () => {
  window.phoneNumber = unMaskedPhoneValue(getPhoneNumberFromUserInput());
  const appVerifier = window.recaptchaVerifier;

  preloadStart();
  firebase.auth().signInWithPhoneNumber(window.phoneNumber, appVerifier)
    .then(confirmationResult => {
      preloaderEnd();
      window.confirmationResult = confirmationResult;
      phoneInputBlock.css('display', 'none');
      codeValidationBlock.css('display', 'block');
      sendButton.classList.remove('send-form-data');
      confirmButton.classList.add('send-form-data');
    })
    .catch(error => {
      phoneValidErrBlock.style.display = 'block';
      console.error(error)
    })
};

confirmButton.onclick = () => {
  const code = getVerificationCode();

  if (code) {
    preloadStart();
    window.confirmationResult.confirm(code)
      .then(result => {
        firebase.auth().currentUser.getIdToken(true)
          .then(idToken => {
            preloaderEnd();
            codeValidationBlock.css('display', 'none');
            backgroundForm.css(
              'background-image', `url(${registerBackgroundImgUrl})`
            );
            backgroundForm.addClass('background-registration');
            registrationBlock.css('display', 'block');
            $('#id_phone_number').val(window.phoneNumber);
            confirmButton.classList.remove('send-form-data');
            registrationButton.classList.add('send-form-data');
          })
          .catch(error => {
            console.error(error);
          })
      })
      .catch(error => {
        codeValidErrBlock.style.display = 'block';
      })
  } else {
    console.log('Укажите код подтверждения!');
  }
};

$(document).on("click", '#registration-button', function (e) {
    e.preventDefault();

    $.ajax({
        url: registrationEndpoint,
        method: 'POST',
        data: $('#register-form').serialize(),
        success: (response) => {
            document.location.href = response['redirect_url'];
        },
        error: (response) => {
            registrationBlock.html(response['responseJSON']['html']);
        }
    })
});

function unMaskedPhoneValue(phone) {
    return phone.replace('(', '').replace(')', '').replace(/-/g, '').replace(/\s/g, '')
}

function getPhoneNumberFromUserInput() {
    return $('input[name="phone"]').val();
}

function getVerificationCode() {
    return $('input[name="code"]').val();
}
