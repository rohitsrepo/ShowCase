angular.module("module.curtainRight")
.controller('rightCurtainController', ['$scope', "auth", function ($scope, auth) {
	'use strict';

	$scope.login = function (user) {
		auth.login(user.email, user.password).then(function (response) {
			console.log("Login request passed:", response);
		}, function (response) {
			console.log("Login request failed:", response);
		});
	};
}]);