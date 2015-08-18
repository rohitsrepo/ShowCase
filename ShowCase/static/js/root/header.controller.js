angular.module('module.root')
.controller('headerController', ['$scope', 'auth', 'uploadmodalService', function ($scope, auth, uploadmodalService) {
	$scope.authorize = function () {
		auth.runWithAuth();
	}

    $scope.showUpload = function () {
        auth.runWithAuth(function () {
            uploadmodalService.showUpload();
        });
    };
}]);