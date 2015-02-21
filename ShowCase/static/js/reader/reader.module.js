angular.module("ReaderApp", ["module.auth", "module.curtainRight", "module.curtainLeft"])
.config(function ($httpProvider) {
	"use strict";

	//Http Intercpetor to check auth failures for xhr requests
    $httpProvider.interceptors.push('authHttpResponseInterceptor');

	// csrf for django
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
}).factory('authHttpResponseInterceptor', ['$q', '$window', function ($q, $window) {
    'use strict';
    
    var loginPrompt = function () {
        if (confirm('Do you wish to login mate!!!')) {
            $window.location.href = '/usersapi-auth/login/';
        }
    };
    
    return {
        responseError: function (response) {
            if (response.status === 403) {
                $window.location.href = "/login";
            }
            return $q.when(reject);
        }
    };
}]).run(['auth', function (auth) {
	auth.getCurrentUser();
}]);