/* Create hours items */
function createBeginTimeHoursItems() {
  let beginTimeContainer = document.getElementById('begin_hour_time_id');
  for (let i = 0; i < 24; i++) {
    let hourDiv = document.createElement('div');
    hourDiv.classList.add('radio');

    let hourInput = document.createElement('input');
    hourInput.id = `hour-begin${i}`;
    hourInput.type = 'radio';
    hourInput.name = 'hour-begin';

    let hourLabel = document.createElement('label');
    hourLabel.htmlFor = `hour-begin${i}`;
    i < 10 ? hourLabel.innerText = `0${i}` : hourLabel.innerText = `${i}`;
    hourDiv.append(hourInput, hourLabel);

    beginTimeContainer.appendChild(hourDiv);
  }
}

function createEndTimeHoursItems() {
  let endTimeContainer = document.getElementById('end_hour_time_id');
  for (let i = 0; i < 24; i++) {
    let hourDiv = document.createElement('div');
    hourDiv.classList.add('radio');

    let hourInput = document.createElement('input');
    hourInput.id = `hour-end${i}`;
    hourInput.type = 'radio';
    hourInput.name = 'hour-end';

    let hourLabel = document.createElement('label');
    hourLabel.htmlFor = `hour-end${i}`;
    i < 10 ? hourLabel.innerText = `0${i}` : hourLabel.innerText = `${i}`;
    hourDiv.append(hourInput, hourLabel);

    endTimeContainer.appendChild(hourDiv);
  }
}

/* Create minutes items */
function createBeginTimeMinutesItems() {
  let endTimeContainer = document.getElementById('select-content__inner_begin_time_id');
  for (let i = 0; i < 60; i++) {
    let minuteDiv = document.createElement('div');
    minuteDiv.classList.add('radio');

    let minuteInput = document.createElement('input');
    minuteInput.id = `minute-begin${i}`;
    minuteInput.type = 'radio';
    minuteInput.name = 'minute-begin';

    let minuteLabel = document.createElement('label');
    minuteLabel.htmlFor = `minute-begin${i}`;
    i < 10 ? minuteLabel.innerText = `0${i}` : minuteLabel.innerText = `${i}`;
    minuteDiv.append(minuteInput, minuteLabel);

    endTimeContainer.appendChild(minuteDiv);
  }
}

function createEndTimeMinutesItems() {
  let endTimeContainer = document.getElementById('select-content__inner_end_time_id');
  for (let i = 0; i < 60; i++) {
    let minuteDiv = document.createElement('div');
    minuteDiv.classList.add('radio');

    let minuteInput = document.createElement('input');
    minuteInput.id = `minute-end${i}`;
    minuteInput.type = 'radio';
    minuteInput.name = 'minute-end';

    let minuteLabel = document.createElement('label');
    minuteLabel.htmlFor = `minute-end${i}`;
    i < 10 ? minuteLabel.innerText = `0${i}` : minuteLabel.innerText = `${i}`;
    minuteDiv.append(minuteInput, minuteLabel);

    endTimeContainer.appendChild(minuteDiv);
  }
}

// Create non fined minutes items
function createNonFinedTimeMinutesItems() {
  let minuteContainer = document.getElementById('non_fined_minute_id');

  for (let i = 0; i < 60; i++) {
    let minuteDiv = document.createElement('div');
    minuteDiv.classList.add('radio');

    let minuteInput = document.createElement('input');
    minuteInput.id = `non-fined-minute${i}`;
    minuteInput.type = 'radio';
    minuteInput.name = 'non-fined-minute';

    let minuteLabel = document.createElement('label');
    minuteLabel.htmlFor = `non-fined-minute${i}`;
    i < 10 ? minuteLabel.innerText = `0${i}` : minuteLabel.innerText = `${i}`;
    minuteDiv.append(minuteInput, minuteLabel);

    minuteContainer.appendChild(minuteDiv);
  }
}
