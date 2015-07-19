angular.module("CompositionApp", [
    'ngSanitize',
    'infinite-scroll',
    "ngAnimate",
    "PostApp",
    "module.auth",
    "module.curtainLeft",
    "module.curtainRight",
    "module.topbar",
    "module.model",
    "module.sharing",
    'module.scrollTo',
    'module.tools',
    'module.titlecase',
    'module.analytics',
    'module.alert'])
.config(['$httpProvider', '$interpolateProvider', function ($httpProvider, $interpolateProvider) {
	"use strict";

    // Changing angular template tag to prevent conflict with django
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

	//Http Intercpetor to check auth failures for xhr requests
    $httpProvider.interceptors.push('authHttpResponseInterceptor');

	// csrf for django
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
}]).factory('authHttpResponseInterceptor', ['$q', '$window', function ($q, $window) {
    'use strict';
    return {
        responseError: function (response) {
            if (response.status === 403) {
                $window.location.href = "/login#?next=" + $window.location.pathname;
            }
            return $q.reject(response);
        }
    };
}]).run(['auth', function (auth) {
	auth.getCurrentUser();
}]);