 /**
 Code that will be executed when dealing with financing sources in the action edit page
 **/

 $( document ).ready(function() {
    /**
    Code that will load when the document is ready
    */
    $('#addMore').on('click', function() {
    /**
        Function executed when click on the add more button, on the financing sources table
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

    $(document).on('click', '.remove', function() {
    /**
        Function executed when clicking on the delete row button, on the financing sources table
    */
        // get the table row
        var trIndex = $(this).closest("tr").index();
        $(this).closest("tr").remove();

    });
});

function showTableRow(rowData=null){
/** Function that shows a table row in the finance sources table
 input: the row data
 */
    console.log('show table row called');
    console.log(rowData);
}