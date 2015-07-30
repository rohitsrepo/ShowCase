angular.module('module.root')
.controller('headerController', ['$scope', 'auth', function ($scope, auth) {
	$scope.authorize = function () {
		auth.runWithAuth();
	}
}]);