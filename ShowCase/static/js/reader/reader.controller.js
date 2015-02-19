angular.module("ReaderApp")
.controller("readerController", ["$scope", "auth", function ($scope, auth) {
	"use strict";

	$scope.$watch(function () {
		return auth.currentUser;
	}, function (currentUser) {
		$scope.currentUser = currentUser;
	});

}]);