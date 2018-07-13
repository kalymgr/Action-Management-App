/*
Javascript file that contains validation rules for the various forms
*/


/**
function that validates phone numbers. Takes as input the form input element that contains the phone number.
It is called by validateFormFields() function
*/
function validatePhoneNumber(el){
    /* if the number of characters is less than 10 */
    if (el.value.length < 10){
        el.setCustomValidity('Ο τηλεφωνικός αριθμός δεν είναι έγκυρος');
    }
    else  /* valid phone number */
    {
        el.setCustomValidity('');
    }

}


/**
Function that validates form fields. It is called on submit
Takes as input the form element.
Calls the other functions that validate form fields
*/
function validateFormFields(formElement){
    /* validate all phone numbers */
    // get all telephone input (declared by using the class 'phone-number')
    phoneNumberInputs = document.getElementsByClassName('phone-number');
    console.log(phoneNumberInputs);
    console.log('the end');

    for (var i=0; i<phoneNumberInputs.length; i++){
        //for each phone number input element, add validation
        validatePhoneNumber(phoneNumberInputs[i]);
        alert(1);
    }

}


