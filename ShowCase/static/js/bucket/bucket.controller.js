angular.module('BucketApp')
.controller('bucketController', ['$scope',
    '$rootScope',
    '$document',
    'auth',
    'bucketModel',
    'bucketmodalService',
    'progress',
    'alert',
    function ($scope, $rootScope, $document, auth, bucketModel, bucketmodalService, progress, alert) {

        $scope.noSuchBucket = {
            status: false,
            action: function () {
                bucketmodalService.showAddToBucket(art);
                close();
            }
        };

        $scope.math = window.Math;
        var currentShowIndex = 0;

        var getArts = function (bucketId) {

            bucketModel.bucketArts(bucketId).then(function (arts) {
                $scope.bucketArts = arts;
                $scope.bucketArts[currentShowIndex].show = true;
                progress.hideProgress();
            }, function () {
                alert.showAlert('We are unable to art for this series');
                progress.hideProgress();
            });
        };

        $scope.bucket = [];
        $scope.init = function (id, name, slug, isWatched, isMe) {
            $scope.bucket.id = id;
            $scope.bucket.slug = slug;
            $scope.bucket.name = name;
            $scope.bucket.isWatched = isWatched == 'True';

            $scope.isMe = isMe == 'True';

            getArts(id);
        };


        $scope.toggleNsfw = function (index) {
            var art = $scope.bucketArts[index];
            art.nsfw = false;
        }

        $scope.nextArt = function () {

            if ($scope.bucketArts.length > currentShowIndex + 1){
                $scope.bucketArts[currentShowIndex].show = false;
                currentShowIndex = currentShowIndex + 1;
                $scope.bucketArts[currentShowIndex].show = true;
            }
        }

        $scope.prevArt = function () {

            if (currentShowIndex > 0){
                $scope.bucketArts[currentShowIndex].show = false;
                currentShowIndex = currentShowIndex - 1;
                $scope.bucketArts[currentShowIndex].show = true;
            }
        }

        $scope.watchBucket = function () {
            auth.runWithAuth(function () {
                progress.showProgress();

                bucketModel.watch($scope.bucket.id).then(function (response) {
                    $scope.bucket.isWatched = true;
                    progress.hideProgress();
                }, function () {
                    progress.hideProgress();
                    alert.showAlert("Unable to complete action");
                });
            });
        };

        $scope.unwatchBucket = function () {
            auth.runWithAuth(function () {
                progress.showProgress();

                bucketModel.unwatch($scope.bucket.id).then(function (response) {
                    $scope.bucket.isWatched = false;
                    progress.hideProgress();
                }, function () {
                    progress.hideProgress();
                    alert.showAlert("Unable to complete action");
                });
            });
        };

        $scope.removeFromBucket = function (index) {
            progress.hideProgress();
            var art = $scope.bucketArts[index];

            bucketModel.removeFromBucket($scope.bucket.id, art.id).then(function () {
                $scope.removeFromSly(index);
                $scope.bucketArts.splice(index, 1);
                progress.hideProgress();
            }, function () {
                progress.hideProgress();
                alert.showAlert('Currently unable to remove this art from the series');
            });
        };

    }
])
.directive('keyEventBinderContentSolo', ['$window', function ($window) {
    return function (scope, element, attrs) {
        element.focus();
        element.bind('keydown', function (evt) {
            scope.slyCallBack(evt);
        });

        scope.$on('$destroy', function () {
            element.unbind('keydown');
        })
    }
}]);