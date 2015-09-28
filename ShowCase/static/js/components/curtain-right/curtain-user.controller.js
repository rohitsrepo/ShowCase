angular.module("module.curtainRight")
.controller('userCurtainController', ['$scope', "auth", 'bucketmodalService', 'uploadmodalService',
    function ($scope, auth, bucketmodalService, uploadmodalService) {
	'use strict';

	$scope.$watch(function () {
		return auth.currentUser;
	}, function (user) {
		$scope.currentUser = user;
	});

    $scope.showCreateBucket = function () {
        bucketmodalService.showCreateBucket();
    };

    $scope.showUpload = function () {
        uploadmodalService.showUpload();
    };

}]);