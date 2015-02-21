angular.module("module.topbar")
.controller("topbarController", ["$scope", "auth", function ($scope, auth) {

	$scope.currentUser = true;

	$scope.$watch(function () {
		return auth.currentUser;
	}, function (currentUser) {
		$scope.currentUser = currentUser;
	});
}]);