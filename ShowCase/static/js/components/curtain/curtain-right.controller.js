angular.module("module.curtain-right", ['model.user'])
.controller('rightCurtainController', ['$scope', 'userModel', function ($scope, userModel) {
	'use strict';

	$scope.loginUser = function (user) {
		userModel.login(user.email, user.password);
	};
}]);