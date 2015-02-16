angular.module("ReaderApp", ["model.user"])
.config(function ($httpProvider) {
	"use strict";

	// csrf for django
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
});