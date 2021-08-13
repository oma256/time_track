'use strict';


function unMaskedPhoneValue(phone) {
    return phone.replace('(', ''
                        ).replace(')', ''
                        ).replace(/-/g, ''
                        ).replace(/\s/g, ''
                        ).replace('+', ''
                        ).replace('____________', '');
}


function feedbackPhoneInputUnMasked(value) {
  return value.replace('(', ''
                      ).replace(')', ''
                      ).replace(/-/g, ''
                      ).replace(/\s/g, ''
                      ).replace('__', '').replace('__', ''
                      ).replace('__', '').replace('__', '')
}