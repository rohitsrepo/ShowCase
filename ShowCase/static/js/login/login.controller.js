angular.module("LoginApp")
.controller("loginController", ["$scope", "auth", 'facebook', '$location', function ($scope, auth, facebook, $location) {
	"use strict";

	$scope.hideLogin = true;

    var next = '/';
    $scope.init = function () {
        next = $location.search()['next'];
    };
    $scope.init();

	$scope.login = function (user) {
		auth.login(user.email, user.password, next).then(function () {
			$scope.loginError = '';
		}, function (error) {
			$scope.loginError = error;
		});
	};

	$scope.loginFB = function () {
    	facebook.login(next).then(function(response){
			$scope.loginError = '';
			}, function (error) {
			$scope.loginError = error;
		})
    };
}]);