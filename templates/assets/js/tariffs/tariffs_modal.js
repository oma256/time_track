'use strict';


const tariffs = document.getElementsByClassName('choice_tariff_btn_class');
const tariffPackagesListBlock = document.getElementById('tariff_model_id');

const showTariffsModal = () => {
  $(".tariffs-modal").addClass("show");
  $(".tariffs-modal .modal").addClass("show");
};

$(document).on("click", '.close-modal-tariffs', function () {
  $(".tariffs-modal").removeClass("show");
  $(".tariffs-modal .modal").removeClass("show");
});

for (let item of tariffs) {
  item.onclick = (event) => {
    const url = new URL(tariffDetailUrl);
    const params = {'tariff_pk': event.currentTarget.id};

    Object.keys(params).forEach(
      key => url.searchParams.append(key, params[key])
    );

    fetch(url, {
      method: 'GET',
      headers: {'Content-Type': 'application/json'}
    })
    .then(handleErrors)
    .then(responseJSON => {
      tariffPackagesListBlock.innerHTML = responseJSON['html'];
      showTariffsModal();
      setEventClickToButtons();
    })
    .catch(error => console.error(error))
  }
}

const setEventClickToButtons = () => {
  const tariffPayButtons = document.getElementsByClassName('tariff-pay-btn');

  for (let btn of tariffPayButtons) {
    btn.onclick = (event) => {
      const data = {
        tariff_pkg_id: parseInt(event.target.parentElement.id),
        org_id: parseInt(organizationId),
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
        window.location.href = responseJSON['paybox_payment_url']
      })
      .catch(error => console.log('error', error))
    }
  }
};
