angular.module("ReaderApp")
.controller("readerController", ["$scope", "auth", function ($scope, auth) {
	"use strict";

	$scope.currentUser = true;

	$scope.$watch(function () {
		return auth.currentUser;
	}, function (currentUser) {
		$scope.currentUser = currentUser;
	});

}]);