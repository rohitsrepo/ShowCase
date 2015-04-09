angular.module("module.curtainRight")
.controller('rightCurtainController', ['$scope', "auth", "$location", 'facebook', function ($scope, auth, $location, facebook) {
	'use strict';

	$scope.login = function (user) {
		auth.login(user.email, user.password, $location.absUrl()).then(function (response) {
			$scope.loginError = '';
		}, function (error) {
			$scope.loginError = error;
		});
	};

    $scope.loginFB = function () {
    	facebook.login($location.absUrl()).then(function(response){
			$scope.loginError = '';
			}, function (error) {
			$scope.loginError = error;
		})
    };

}]);