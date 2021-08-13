'use strict';

// Download employee excel report file
const downloadBtn = document.getElementById('download-btn_id');
let startTime = null;
let endTime = null;

downloadBtn.onclick = () => {
  const url = new URL(reportDownloadUrl);
  const xhttp = new XMLHttpRequest();

  if (startTime !== null && endTime !== null) {
    const params = {
      start_time: startTime,
      end_time: endTime
    };

    Object.keys(params).forEach(key => {
      url.searchParams.append(key, params[key])
    });
  }

  xhttp.open('GET', url, true);
  xhttp.setRequestHeader('Content-Type', 'application/json');
  xhttp.responseType = 'blob';
  xhttp.send();
  xhttp.onreadystatechange = () => {
    let a, today;
    if (xhttp.readyState === 4 && xhttp.status === 200) {
      today = new Date();
      a = document.createElement('a');
      a.href = window.URL.createObjectURL(xhttp.response);
      a.download = `work_times_${
        today.toDateString().split(' ').join('_')
      }.xls`;
      a.style.display = 'none';

      document.body.appendChild(a);

      return a.click();
    }
  };
};


// Print employee report
const printBtn = document.getElementById('print-btn_id');
const reportTemplateBlock = document.getElementById('report_template_block_id');

printBtn.onclick = () => {
  const url = new URL(reportPrintUrl);

  if (startTime !== null && endTime !== null) {
    const params = {
      start_time: startTime,
      end_time: endTime
    };

    Object.keys(params).forEach(key => {
      url.searchParams.append(key, params[key])
    });
  }

  fetch(url, {
    method: 'GET',
    headers: {
      'Content-type': 'application/json',
    }
  })
  .then(handleErrors)
  .then(responseJSON => {
    reportTemplateBlock.innerHTML = responseJSON['html'];
    const printWindow = window.open('', 'PrintMap', 'width=' + 1200 + ',height=' + 700);

    printWindow.document.writeln(reportTemplateBlock.innerHTML);
    printWindow.document.close();
    printWindow.print();
  })
  .catch(error => console.log('error', error));
};
