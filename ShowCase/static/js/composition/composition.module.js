angular.module("CompositionApp", ["module.auth", "module.curtainLeft", "module.curtainRight", "module.topbar"])
.config(function ($httpProvider) {
	"use strict";

	//Http Intercpetor to check auth failures for xhr requests
    $httpProvider.interceptors.push('authHttpResponseInterceptor');

	// csrf for django
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
}).factory('authHttpResponseInterceptor', ['$q', '$window', function ($q, $window) {
    'use strict';
    return {
        responseError: function (response) {
            if (response.status === 403) {
                $window.location.href = "/login";
            }
            return $q.reject(response);
        }
    };
}]).run(['auth', function (auth) {
	auth.getCurrentUser();
}]);