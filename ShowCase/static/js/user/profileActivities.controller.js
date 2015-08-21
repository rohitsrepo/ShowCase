angular.module('UserApp')
.controller('profileActivitiesController', ['$scope',
    'activityModel',
    'bucketmodalService',
    'bookService',
    'usermodalService',
    'progress',
    'alert',
    function ($scope, activityModel, bucketmodalService, bookService, usermodalService, progress, alert) {

        $scope.math = window.Math;

        progress.showProgress();
        activityModel.userActivities($scope.artist.id).then(function (reponse) {
            $scope.userActivities = reponse.results;
            progress.hideProgress();
        }, function () {
            alert.showAlert('We are unable to fetch data');
            progress.hideProgress();
        });

        $scope.showBucketArts = function (index) {
            var activity = $scope.userActivities[index];
            bucketmodalService.showBucketArts(activity.content);
        };

        $scope.handleBookMark = function (index) {
            art = $scope.userActivities[index].composition;
            if (art.is_bookmarked) {
                bookService.unmark(art).then(function () {
                    art.is_bookmarked = false;
                });
            } else {
                bookService.bookmark(art).then(function () {
                    art.is_bookmarked = true;
                });;
            }
        };

        $scope.showBookMarkers = function (index) {
            var art = $scope.userActivities[index].composition;

            usermodalService.showBookMarkers(art).then(function (bookStatus) {
                if (bookStatus == 'bookmarked') {
                    art.is_bookmarked = true;
                }
            });
        };

        $scope.showArtBuckets = function (index) {
            var art = $scope.userActivities[index].composition;
            bucketmodalService.showArtBuckets(art);
        }

        $scope.showAddToBucket = function (index) {
            var art = $scope.userActivities[index].composition;
            bucketmodalService.showAddToBucket(art);
        };
    }
]);