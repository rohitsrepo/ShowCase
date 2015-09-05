angular.module('module.root')
.controller('headerController', ['$scope', '$window', '$location', 'auth', 'uploadmodalService', function ($scope, $window, $location, auth, uploadmodalService) {

    $scope.exploreActive = false;
    $scope.postsActive = false;

    function initActiveLink() {
        path = window.location.pathname;

        if (path=='/arts') {
            $scope.exploreActive = true;
        } else if (path=='/posts') {
            $scope.postsActive = true;
        }
    };
    initActiveLink();

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

    $scope.gotoMySeries = function () {
        auth.getCurrentUser().then(function (user) {
            $window.location.href = '/@' + user.slug + '/series';
        });
    };
}])
.directive('customHref', [function () {
    return function (scope, element, attrs) {
        element.bind('click', function () {
            window.location.href = attrs['customHref'];
        })

    };
}]);