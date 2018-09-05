 /**
 Code that will be executed in the action edit page
 **/

var ActionFinancingTable = function(){
	/**
	Javascript class for handling the action financing table
	*/
	
	this.tableHtmlId = "#sourcesOfFinanceTb";
	this.newRow = "<tr><td> <select name='financingSource' class='custom-select financingSource'>" +
        "<option>-</option>{%  for finSource in financingSources %}<option value='{{ finSource.id }}'>{{ finSource.name }}</option>" +
        "{%  endfor %}</select></td><td><input type='text' name='financingSourceBudgetCode' class='form-control'></td>" +
        "<td><input type='text' name='financingSourceAmount' class='form-control'></td>" +
        "<td><a href='javascript:void(0);'  class='remove'><span class='fas fa-trash'></span></a></td></tr>";
};

ActionFinancingTable.prototype.showTableRows = function(actionId){
	/**
	Class method that shows the table rows. Takes as parameter the action id
	*/
	console.log('show table row called');
    console.log(actionId);
	
    var url = '/actions/'+actionId+'/financingsources_json';
    jQuery.getJSON(url, function( data ){
        console.log('ajax success');
        console.log(data);
		
		// for each financing source, populate the html code and append to the table
    });
}; 

ActionFinancingTable.prototype.setRow = function(rowData, financingSources){
	/**
	Class method that creates and returns the row html code.
	Parameters: the row data for the specific action and the financing sources, 
	to populate the select box
	Returns the row html code
	*/
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
        // create a new row
        var newRow = "<tr><td> <select name='financingSource' class='custom-select financingSource'>" +
        "<option>-</option>{%  for finSource in financingSources %}<option value='{{ finSource.id }}'>{{ finSource.name }}</option>" +
        "{%  endfor %}</select></td><td><input type='text' name='financingSourceBudgetCode' class='form-control'></td>" +
        "<td><input type='text' name='financingSourceAmount' class='form-control'></td>" +
        "<td><a href='javascript:void(0);'  class='remove'><span class='fas fa-trash'></span></a></td></tr>";

        var table = $("#sourcesOfFinanceTb");
        table.append(newRow);

        console.log('prosthiki row button clicked');
    });

    $(document).on('click', '.removeFinancingSource', function() {
    /**
        Function executed when clicking on the delete row button, on the financing sources table
    */
        // get the table row
        var trIndex = $(this).closest("tr").index();
        $(this).closest("tr").remove();

    });
});


 function loadFinancingSourcesTable(actionId){
	/**
	Method that loads the financing sources of an action.
	*/
	actionFinTable.showTableRows(actionId);
}