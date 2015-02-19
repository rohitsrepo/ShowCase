angular.module("ReaderApp", ["module.auth", "module.curtainRight", "module.curtainLeft"])
.config(function ($httpProvider) {
	"use strict";

	// csrf for django
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
}).run(['auth', function (auth) {
	auth.getCurrentUser();
}]);