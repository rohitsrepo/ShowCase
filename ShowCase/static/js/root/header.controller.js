angular.module('module.root')
.controller('headerController', ['$scope',
    '$window',
    '$location',
    'auth',
    'uploadmodalService',
    'bucketmodalService',
    function ($scope, $window, $location, auth, uploadmodalService, bucketmodalService) {

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

    $scope.gotoMyBookmarks = function () {
        auth.getCurrentUser().then(function (user) {
            $window.location.href = '/@' + user.slug + '/bookmarks';
        });
    };

    $scope.gotoMyContributions = function () {
        auth.getCurrentUser().then(function (user) {
            $window.location.href = '/@' + user.slug + '/contributions';
        });
    };

    $scope.showCreateBucket = function () {
        bucketmodalService.showCreateBucket();
    };

}])
.directive('customHref', [function () {
    return function (scope, element, attrs) {
        element.bind('click', function () {
            window.location.href = attrs['customHref'];
        })

    };
}])
.directive('siteLoader', [function () {
    return {
        restrict: 'E',
        replace: true,
        scope: {
            siteLoaderHide: '='
        },
        template: '<div class="site-loader" ng-cloak ng-hide="siteLoaderHide"><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span></div>'
    };
}]);