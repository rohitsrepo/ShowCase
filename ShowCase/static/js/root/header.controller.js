angular.module('module.root')
.controller('headerController', ['$scope', '$window', 'auth', 'uploadmodalService', function ($scope, $window, auth, uploadmodalService) {
	$scope.authorize = function () {
		auth.runWithAuth();
	}

    $scope.showUpload = function () {
        uploadmodalService.showUpload();
    };

    $scope.goHome = function () {
        auth.getCurrentUser().then(function (user) {
            $window.location.href = '/@' + user.slug;
        });
    };
}]);