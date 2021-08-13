const buttonDepartmentAddInput = document.getElementById('button-add-input_id');
const filialNameInput = document.getElementById('filial-name-input_id');
const saveButton = document.getElementById('save-button_id');
const successMsgBlock = document.getElementById('success-saved-msg_id');
const nameErrorMsgBlock = document.getElementById('name-error_id');
let departmentNameList = [];
let filialData = {};
// default map set latitude and longitude
let map_lat = 42.882004;
let map_lng = 74.582748;
let filialLocation = false;

const getDepartmentName = () => document.getElementById('department-input_id').value;

const getDepartmentListDivBlock = () => document.getElementById('department-list_id');

const createDepartmentLabel = () => {
  const label = document.createElement('label');
  label.innerText = getDepartmentName();

  return label
};

const createDepartmentDiv = () => {
  const div = document.createElement('div');
  div.classList.add('radio');

  return div
};

$(document).ready(() => {
  const div = $(".open-modal__location");
  const con = $(".modal-location__content");
  const div2 = $(".open-modal__location-two");
  const con2 = $(".modal-location__content-two");
  const body = $("body");

  div.click(() => {
    con.css("visibility", "visible");
    body.addClass("body-overflow");
  });

  $(".close-modal-location").click(() => {
    con.css("visibility", "hidden");
    body.removeClass("body-overflow")
  });


  div2.click(() => {
    con2.css("visibility", "visible");
    body.addClass("body-overflow")
  });

  $(".close-modal-location").click(() => {
    con2.css("visibility", "hidden");
    body.removeClass("body-overflow")
  })
});

filialNameInput.onkeyup = event => {
  if (event.target.value) {
    if (filialLocation) {
      saveButton.removeAttribute('disabled');
    } else {
      saveButton.setAttribute('disabled', 'disabled');
    }
  } else {
    saveButton.setAttribute('disabled', 'disabled');
  }
};

saveButton.onclick = () => {
  filialData['filial_name'] = filialNameInput.value;
  filialData['departments_names'] = departmentNameList;
  filialData['org_id'] = orgID;

  fetch(filialDepartmentCreateEndpoint, {
    method: 'POST',
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(filialData),
  }).then((response) => {
    response.status === 201
      ? successMsgBlock.style.display = 'flex'
      : console.log('input error')
  })
  .catch(error => console.error(error.statusText))
};

buttonDepartmentAddInput.onclick = () => {
  let departmentBlock = $('#department-block_id');
  let departmentListBlock = getDepartmentListDivBlock();
  let departmentDivBlock = createDepartmentDiv();
  let departmentLabel = createDepartmentLabel();

  departmentDivBlock.appendChild(departmentLabel);

  if (!departmentNameList.includes(getDepartmentName())) {
    departmentNameList.push(getDepartmentName());
    departmentListBlock.appendChild(departmentDivBlock);
    departmentBlock.height((index, height) => height + 50);
    nameErrorMsgBlock.style.display = 'none';
  } else {
    nameErrorMsgBlock.style.display = 'block';
  }
};

DG.then(() => {
  const map = DG.map('map', {
    center: [map_lat, map_lng],
    zoom: 13
  });
  let marker;

  map.on('click', (e) => {
    filialData['location'] = {lat: e.latlng.lat, lng: e.latlng.lng};

    if (!marker) {
      marker = DG.marker([e.latlng.lat, e.latlng.lng], {
        'draggable': true
      }).addTo(map);
    } else {
      marker.setLatLng([e.latlng.lat, e.latlng.lng]);
    }

    document.getElementById('location-error-msg_id').innerText = '';

    filialLocation = true;

    if (filialNameInput.value) {
      saveButton.removeAttribute('disabled');
    } else {
      saveButton.setAttribute('disabled', 'disabled');
    }

  })
});
