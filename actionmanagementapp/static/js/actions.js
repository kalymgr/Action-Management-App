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
actionApp.controller('actionCtrl', function($scope, $http) {
	
	// Data
	$scope.action = new Action();  // action data
	$scope.actionParameters = new ActionParameters();  // various parameters
	$scope.services = [];  // list of services. Used in dropdown boxes
	$scope.actionCategories = [];  // list of action categories. Used in dropdown boxes
	$scope.actionGroups = [];
	$scope.newOrInProgressList = $scope.actionParameters.newOrInProgressList;
	$scope.priority = $scope.actionParameters.priority;
	$scope.status = $scope.actionParameters.status;
	$scope.financingSources = null;
	
	// Functions that load data

	$scope.loadAction = function(actionId){
		/**
		Function that loads action data from the database. Uses ajax
		*/

		$http.get('/actions/' + actionId + '/json')
			.then(function(response){
			$scope.action.id = response.data.id;
			$scope.action.name = response.data.name;
			$scope.action.serviceInChargeId = response.data.serviceInChargeId;
			$scope.action.implementationServiceId = response.data.implementationServiceId;
			$scope.action.categoryId = response.data.categoryId;
			$scope.action.newOrInProgress = response.data.newOrInProgress;
			$scope.action.priority = response.data.priority;
			$scope.action.groupId = response.data.groupId;
			$scope.action.budget = response.data.budget;
			$scope.action.budgetCode = response.data.budgetCode;
			$scope.action.startDate = new Date(response.data.startDate);
			$scope.action.endDate = new Date(response.data.endDate);
			$scope.action.status = response.data.status;
			$scope.action.details = response.data.details;
		});
	}
	
	$scope.loadServices = function()
	{
		/**
		Function that loads services data from the database. Uses ajax.
		Must be called after document is loaded.
		*/
		$http.get('/org/services/json')
			.then(function(response){
				$scope.services = response.data;
		});
	}
	
	$scope.loadActionCategories = function()
	{
		/**
		Function that loads action categories data from the database. Uses ajax.
		Must be called after document is loaded.
		*/
		$http.get('/actions/action_categories/json')
			.then(function(response){
				$scope.actionCategories = response.data;
		});
	}

	$scope.loadActionGroups = function()
	{
		/**
		 * Function that loads action groups data from the database. Uses ajax.
		 * Must be called after document is loaded.
		 */
		$http.get('/actions/action_groups/json')
			.then(function(response){
				$scope.actionGroups = response.data;
		});
	}

	$scope.loadFinancingSources = function()
	{
		/**
		 * Function that loads financing sources data from the database. Uses ajax.
		 * Must be called after document is loaded.
		 */
		$http.get('/actions/financingsources_json')
			.then(function(response){
				$scope.financingSources = response.data;
			});
	}


	// Variables and Functions that generate html code
	$scope.formHtmlId = 'actionCtrl';  // html id of the form element
	$scope.financingSourcesTableHtmlId = "#sourcesOfFinanceTb";  // HTML id of the table element


	$scope.showFinancingSourcesTableRows = function(actionId)
	{
		/**
		 Method that loads from the database and shows the table rows. Takes as parameter the action id
		 */

		$http.get('/actions/'+actionId+'/financingsources_json')
			.then(function(response){
				$scope.action.actionFinancingSources = response.data;
				var actionFinancingSources = null;  // list of financing sources of the specific action

				// build and add to the financing sources table a row, for each financing source
				for (var i=0; i<$scope.action.actionFinancingSources.length;i++){
					$scope.setFinancingSourcesRow($scope.action.actionFinancingSources[i]);
				}
			});


	}

	$scope.setFinancingSourcesRow = function(rowData)
	{
		/**
		 Class method that creates and returns the row html code.
		 Parameters: the row data for the specific action and the financing sources,
		 to populate the select box
		 Returns the row html code
		 */

		// create the table row with the rowData, or create a new table row if null

		var financingSources = $scope.financingSources;

		if (rowData == null)
		{

			// set some rowData for a new row
			rowData = {
				'actionId': 0,
				'amount': 0,
				'budgetCode': '0',
				'financingSourceId': 0,
			};
		}
		var tableRow = "<tr><td><select name='financingSource' ";
		tableRow += "class='custom-select financingSource' ng->";

		tableRow += "</td><td><input type='text' name='financingSourceBudgetCode'" +
		" class='form-control' value='" + rowData['budgetCode'] + "'>" +
		" </td><td><input type='text' name='financingSourceAmount' class='form-control'" +
		"value='" + rowData['amount'] + "'></td><td><a href='javascript:void(0);' " +
		"class='removeFinancingSource'><span class='fas fa-trash'></span></a></td></tr>" ;

		// add the table row to the table
		var table = $(this.tableHtmlId);
		table.append(tableRow);
	}


}); 


$( document ).ready(function()
{
    /**
    Code that will load when the document is ready
    */
	
    $('#addMorefinancingSources').on('click', function() {
    /**
        Function executed when clicking on the add more button, on the financing sources table
    */


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
		validateFormFields(event.currentTarget);
		saveAction();
	});
});
