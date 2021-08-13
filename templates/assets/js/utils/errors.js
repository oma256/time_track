'use strict';


function handleErrors(response) {
  if (response.ok) {
    return  response.json();
  }
  return Promise.reject(response);
}