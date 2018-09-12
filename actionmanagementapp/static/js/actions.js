 /**
 Code that will be executed in the action edit page
 **/


/** angular.js code for managing actions */
// create the action app object
var actionApp = angular.module('actionApp', []);

// change from {{ }} to {a  a} so as not to clash with jinja templates brackets
actionApp.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);

// setup the angular.js controller of the app
actionApp.controller('actionCtrl', function($scope) {
    $scope.firstName= "John";
    $scope.lastName= "Doe";
}); 



var ActionFinancingTable = function(){
	/**
	Javascript class for handling the action financing table
	*/
	
	this.tableHtmlId = "#sourcesOfFinanceTb";  // CSS id of the html table
	this.financingSources = null;
};

ActionFinancingTable.prototype.showTableRows = function(actionId){
	/**
	Class method that shows the table rows. Takes as parameter the action id
	*/	
	
	// var financingSources = null;  // list of financing sources
	var actionFinancingSources = null;  // list of financing sources of the specific action
	var actionFinancingTableObject = this;

	// get the list of the financing sources available
	jQuery.ajax({
		url: '/actions/financingsources_json',
		dataType: 'json',
		async: false,
		success: function(finSourcesJson) {
			actionFinancingTableObject.financingSources = finSourcesJson;
		}
	});
	
	// get the financing sources of the specific action
	jQuery.ajax({
		url: '/actions/'+actionId+'/financingsources_json',
		dataType: 'json',
		async: false,
		success: function(actionFinSourcesJson) {
			actionFinancingSources = actionFinSourcesJson;
		}
	});
	
	// build and add to the financing sources table a row, for each financing source
	// console.log(financingSources);
	// console.log(actionFinancingSources);
	for (var i=0; i<actionFinancingSources.length;i++){
	    this.setRow(actionFinancingSources[i], actionFinancingTableObject.financingSources);
	}
}; 

ActionFinancingTable.prototype.setRow = function(rowData, financingSources){
	/**
	Class method that creates and returns the row html code.
	Parameters: the row data for the specific action and the financing sources, 
	to populate the select box
	Returns the row html code
	*/

	// create the table row with the rowData, or create a new table row if null

	if (rowData == null)
	{
		console.log('New row');
	    // set some rowData for a new row
	    rowData = {
	        'actionId': 0,
	        'amount': 0,
	        'budgetCode': '0',
	        'financingSourceId': 0,
	    };
	}
	var tableRow = "<tr><td><select name='financingSource' class='custom-select financingSource'><option>-</option>";
	for (var key in financingSources){
		console.log(financingSources[key]);
	    if (key == rowData['financingSourceId']){  // if the element is selected
	        tableRow += "<option value='" + rowData['financingSourceId'] +
	        "' selected>" + financingSources[key] + "</option>";
	    }
	    else {  // the element is not selected
	        tableRow += "<option value='" + rowData['financingSourceId'] +
	        "'>" + financingSources[key] + "</option>";
	    }
	}
    tableRow += "</select></td><td><input type='text' name='financingSourceBudgetCode'" +
        " class='form-control' value='" + rowData['budgetCode'] + "'>" +
        " </td><td><input type='text' name='financingSourceAmount' class='form-control'" +
        "value='" + rowData['amount'] + "'></td><td><a href='javascript:void(0);' " +
        "class='removeFinancingSource'><span class='fas fa-trash'></span></a></td></tr>" ;

    // add the table row to the table
    var table = $(this.tableHtmlId);
    table.append(tableRow);
}


// create a new object for the financing table
var actionFinTable = new ActionFinancingTable();


$( document ).ready(function() {
    /**
    Code that will load when the document is ready
    */
		
		
    $('#addMorefinancingSources').on('click', function() {
    /**
        Function executed when clicking on the add more button, on the financing sources table
    */
        actionFinTable.setRow(null, actionFinTable.financingSources);

    });

	
    $(document).on('click', '.removeFinancingSource', function() {
    /**
        Function executed when clicking on the delete row button, on the financing sources table
    */
        // get the table row
        var trIndex = $(this).closest("tr").index();
        $(this).closest("tr").remove();

    });
	
	
	/** add event handlers */
	jQuery(document).on('click', '#saveActionButton', function(event){
		console.log('something');
		validateFormFields(event.currentTarget);
		saveAction();
	});
});


 function loadFinancingSourcesTable(actionId){
	/**
	Function that loads the financing sources of an action.
	*/
	actionFinTable.showTableRows(actionId);
}


function saveAction(){
	/**
	Function responsible for saving the action data in the database
	*/
	
	
}