/*
Javascript file that contains validation rules for the various forms
*/


/**
function that validates phone numbers. Takes as input the form input element that contains the phone number.
It is called by validateFormFields() function
*/
function validatePhoneNumber(el){
	
    /* in order for a phone number to be valid, it must have at least 10 digits. 
	Also, only digits and spaces are allowed. This means that the sum of the number of digits and the number of spaces
	should be equal to the total number of characters*/
	
	//get the length of the phone number
	var phoneNumberLength = el.value.length;
	//get the number of digits
	if (el.value.match(/\d/g))
		var digitsNumber = el.value.match(/\d/g).length;
	else  // if regexp result is null, set to zero
		var digitsNumber = 0;
	
	//get the number of spaces
	if (el.value.match(/ /g))
		var spacesNumber = el.value.match(/ /g).length;
	else // if regexp result is null, set to zero
		var spacesNumber = 0;
	
	// if the user has typed a phone number and it is invalid
    if ( (phoneNumberLength>0) && ((phoneNumberLength < 10) || (phoneNumberLength != digitsNumber+spacesNumber)) )
	{
		// set the message, for the invalid phone number
		el.setCustomValidity('Ο τηλεφωνικός αριθμός δεν είναι έγκυρος. Χρησιμοποιείστε μόνο ψηφία (τουλάχιστον 10) και κενά. ');
		
    }
    else  // the user hasn't typed a phone number or the phone number typed is valid. Reset the validity
    {
		el.setCustomValidity('');
    }
}


/**
Function that validates form fields. It is called on submit
Takes as input the ok button element.
Calls the other functions that validate form fields
*/
function validateFormFields(okButtonElement){
	
	// get the form object
	formObj = okButtonElement.form;
	
    /* validate all phone numbers */
	
    // get all form input objects
    formInputs = formObj.getElementsByTagName('input');
    

    for (var i=0; i<formInputs.length; i++){
        //for each phone number (that has tel as type), add validation
		if (formInputs[i].type == 'tel')
		{
			validatePhoneNumber(formInputs[i]);
		}
    }

}


