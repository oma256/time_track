'use strict';


const globalSearchInput = document.getElementById('global_search_input_id');
const globalSearchResultBlock = document.getElementById('search-result__content_id');


globalSearchInput.addEventListener('keyup', (event) => {
  const url = new URL(globalSearchUsersEndpoint);
  const params = {'name': event.target.value};

  Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

  setTimeout(() => {
    if (params.name) {
      fetch(url, {
        method: 'GET',
        headers: {'Content-Type': 'application/json'},
      })
      .then(response => response.json())
      .then(responseJSON => globalSearchResultBlock.innerHTML = responseJSON['html'])
      .catch(error => console.log(error))
    }
  }, 1000)
});

