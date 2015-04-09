angular.module("LoginApp")
.controller("loginController", ["$scope", "auth", 'facebook', function ($scope, auth, facebook) {
	"use strict";

	$scope.hideLogin = true;

	$scope.login = function (user) {
		auth.login(user.email, user.password).then(function () {
			$scope.loginError = '';
		}, function (error) {
			$scope.loginError = error;
		});
	};

	$scope.loginFB = function () {
    	facebook.login('/').then(function(response){
			$scope.loginError = '';
			}, function (error) {
			$scope.loginError = error;
		})
    };
}]);