/**
This file contains the javascript classes that correspond to the database models related to actions
*/

var Action = function(){
	/**
	Javascript class for handling actions
	*/
	this.id;
	this.name;
	this.serviceInChargeId;
	this.implementationServiceId;
	this.categoryId;
	this.newOrInProgress;
	this.priority;
	this.groupId;
	this.budget;
	this.budgetCode;
	this.startDate;
	this.endDate;
	this.status;
	this.details;
	this.actionFinancingSources = [];
}


var FinancingSource = function(){
	/**
	Javascript class for handling financing sources
	*/
	this.id;
	this.name;
	this.details;
}


var ActionFinancingSource = function(){
	/**
	Javascript class for handling financing sources for the action
	*/
	this.actionId;
	this.financingSourceId;
	this.budgetCode;
	this.amount;
}


var ActionCategory = function(){
	/**
	Javascript class for handling action categories for the action
	*/
	this.id;
	this.name;
}

var ActionParameters = function(){
	/**
	 * Javascript class for handling various parameters data
	 * for the action
	 */
	this.newOrInProgressList =
	[
		'Νέα',
		'Συνεχιζόμενη'
	];
	this.priority = [
		'(1) Υψηλή',
		'(2) Μεσαία',
		'(3) Χαμηλή'
	];
	this.status = [
		'Δεν έχει ξεκινήσει',
		'Σε εξέλιξη',
		'Ολοκληρώθηκε',
		'Αναβλήθηκε',
		'Σε αναμονή'
	]
}