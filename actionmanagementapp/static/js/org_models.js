/**
This file contains the javascript classes that correspond to the database models related to organizations and services
*/


var Organization = function()
{
	/**
	Javascript class for handling organizations
	*/
	
	this.id;
	this.name;
	this.type;
	this.address;
	this.ceo;
	this.phone;
	this.email;
	this.irsNo;
	this.logoPath;
	this.parentOrganizationId;
}


var Service = function()
{
	/**
	Javascript class for handling services
	*/
	
	this.id;
	this.name;
	this.address;
	this.chief;
	this.phone;
	this.email;
	this.parentServiceId;
	this.organizationId;
	this.type;
}


var OrganizationType = function()
{
	/**
	Javascript class for handling Organization types
	*/
	this.id;
	this.name;
}


var ServiceType = function()
{
	/**
	Javascript class for handling service types
	*/
	this.id;
	this.name;
}


