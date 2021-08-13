'use strict';


const settingsButton = document.getElementById('settings-button_id');

const getBeginHour = () => parseInt(document.getElementById('begin-hour_id').innerText);
const getBeginMinute = () => parseInt(document.getElementById('begin-min_id').innerText);
const getEndHour = () => parseInt(document.getElementById('end-hour_id').innerText);
const getEndMinute = () => parseInt(document.getElementById('end-min_id').innerText);
const getNonFinedMin = () => parseInt(document.getElementById('non-fined-min_id').innerText);
const setSettingTimesData = () => {
  settingData.begin_hour = getBeginHour();
  settingData.begin_min = getBeginMinute();
  settingData.end_hour = getEndHour();
  settingData.end_min = getEndMinute();
  settingData.non_fined_min = getNonFinedMin();
};

(function () {
  createBeginTimeHoursItems();
  createEndTimeHoursItems();
  createBeginTimeMinutesItems();
  createEndTimeMinutesItems();
  createNonFinedTimeMinutesItems();
})();

// Company settings set geolocation in map

let marker;

DG.then(() => {
  const map = DG.map('map', {
    center: [company_lat, company_lng],
    zoom: 13
  });

  DG.marker([company_lat, company_lng])
    .addTo(map)
    .bindPopup('Локация компании!');

  map.on('click', (e) => {
    settingData.location = {lat: e.latlng.lat, lng: e.latlng.lng};
    if (!marker) {
      marker = DG.marker([e.latlng.lat, e.latlng.lng], {
        'draggable': true
      }).addTo(map);
    } else {
      marker.setLatLng([e.latlng.lat, e.latlng.lng]);
    }
    document.getElementById('location-error-msg_id').innerText = '';
    document.getElementById('settings-button_id').removeAttribute('disabled');
  })
});


$(document).ready(function () {
  let div = $(".open-modal__location");
  let con = $(".modal-location__content");
  let div2 = $(".open-modal__location-two");
  let con2 = $(".modal-location__content-two");
  let body = $("body");

  div.click(function () {
    con.css("visibility", "visible");
    body.addClass("body-overflow");
  });

  $(".close-modal-location").click(function () {
    con.css("visibility", "hidden");
    body.removeClass("body-overflow")
  });


  div2.click(function () {
    con2.css("visibility", "visible");
    body.addClass("body-overflow")
  });

  $(".close-modal-location").click(function () {
    con2.css("visibility", "hidden");
    body.removeClass("body-overflow")
  })

});

/* Send settings data to server by click save button */
settingsButton.onclick = (() => {

  setSettingTimesData();

  fetch(organizationSettingEndpoint, {
    method: 'POST',
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(settingData),
  })
  .then((response) => {
    if (response.ok) {
      return response.json();
    } else {
      console.error('Ошибка вводных данных');
    }
  })
  .then(responseJSON => {
    if (responseJSON['employee_exist']) {
      window.location.reload(true);
    } else {
      window.location.href = responseJSON['redirect_url'];
    }
  })
  .catch(error => {
    console.error('error:', error);
  })
});

document.querySelectorAll('.print').forEach(item => {
  item.children[0].addEventListener('click', () => {
    const qrCodeContainer = item.children[0].parentNode.parentNode.children[0];
    const printWindow = window.open('', 'PrintMap', 'width=' + 1200 + ',height=' + 700);

    printWindow.document.writeln(qrCodeContainer.innerHTML);
    printWindow.document.close();
    printWindow.print();
  });
});


document.querySelectorAll('.download').forEach(item => {
  item.children[0].addEventListener('click', (event) => {
    const url = new URL(organizationQrCodeDownloadUrl);
    const params = {'org_pk': event.currentTarget.id};

    Object.keys(params).forEach(
      key => url.searchParams.append(key, params[key])
    );

    fetch(url, {
      method: 'GET',
      contentType: 'application/json',
    })
    .then(response => response.json())
    .then(responseJSON => {
      const a = document.createElement('a');
      a.href = responseJSON['qr_code_url'];
      a.setAttribute('download', "download");
      document.body.appendChild(a);

      return a.click();
    })
  })
});

document.querySelectorAll('.print').forEach(item => {
  item.children[0].addEventListener('click', () => {
    const qrCodeContainer = item.children[0].parentNode.parentNode.children[0];
    const printWindow = window.open('', 'PrintMap', 'width=' + 1200 + ',height=' + 700);

    printWindow.document.writeln(qrCodeContainer.innerHTML);
    printWindow.document.close();
    printWindow.print();
  });
});


document.querySelectorAll('.download').forEach(item => {
  item.children[0].addEventListener('click', (event) => {
    const qrCodeContainer = item.children[0].parentNode.parentNode.children[0];
    const a = event.currentTarget;
    a.href = qrCodeContainer.children[0].src;
    a.onclick();
  })
});
