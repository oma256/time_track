'use strict';


// Returns the cookie value by name
const getCookie = (name) => {
    return document.cookie.split(';').reduce((prev, c) => {
        let arr = c.split('=');
        return (arr[0].trim() === name) ? arr[1] : prev;
    }, undefined);
};
