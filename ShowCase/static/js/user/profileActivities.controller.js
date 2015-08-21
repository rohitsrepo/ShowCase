angular.module('UserApp')
.controller('profileActivitiesController', ['$scope',
    'activityModel',
    'bucketmodalService',
    'bookService',
    'usermodalService',
    'progress',
    'alert',
    function ($scope, activityModel, bucketmodalService, bookService, usermodalService, progress, alert) {

        $scope.userActivities = [];
        $scope.activitiesMeta = {next_token: '', disableGetMore: false, busy: false, noActivities: false};

        var getActivities = function () {

            if (!$scope.activitiesMeta.disableGetMore) {
                var next_token = $scope.activitiesMeta.next_token;
                progress.showProgress();
                activityModel.userActivities($scope.artist.id, next_token).then(function (response) {
                    $scope.activitiesMeta.next_token = response.next_token;

                    for (var i = 0; i < response.results.length; i++) {
                        $scope.userActivities.push(response.results[i]);
                    }

                    if (response.next_token == ""){
                        $scope.activitiesMeta.disableGetMore = true;
                    }

                    if ($scope.userActivities.length == 0){
                        $scope.activitiesMeta.noActivities = true;
                    }

                    progress.hideProgress();
                    $scope.activitiesMeta.busy = false;
                }, function () {
                    alert.showAlert('We are unable to fetch data');
                    progress.hideProgress();
                });
            }
        };

        $scope.loadMoreActivities = function () {
            if ($scope.activitiesMeta.busy) {
                return;
            }

            $scope.activitiesMeta.busy = true;
            getActivities();
        };

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