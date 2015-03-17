angular.module("module.curtainRight")
.controller('rightCurtainController', ['$scope', "auth", "$location", function ($scope, auth, $location) {
	'use strict';

	$scope.login = function (user) {
		auth.login(user.email, user.password, $location.absUrl()).then(function (response) {
			$scope.loginError = '';
		}, function (error) {
			$scope.loginError = error;
		});
	};
}]);