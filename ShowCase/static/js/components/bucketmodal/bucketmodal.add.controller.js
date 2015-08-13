angular.module('module.bucketmodal')
.controller('bucketmodalAddController', ['$scope',
    'bucketModel',
    'bucketmodalService',
    'close',
    'art',
    'user',
    'progress',
    'alert',
    function ($scope, bucketModel, bucketmodalService, close, art, user, progress, alert) {

        $scope.noUserBucket = {
            status: false,
            action: function () {}
        }

        progress.showProgress();
        $scope.art = art;
        bucketModel.userBuckets(user.id).then(function (buckets) {
            $scope.userBuckets = buckets;

            if ($scope.userBuckets.length == 0){
                $scope.noUserBucket.status = true;
            }

            progress.hideProgress();
        }, function () {
            alert.showAlert('We are unable to fetch data');
            progress.hideProgress();
        });

        $scope.addToThisBucket = function (index) {
            progress.showProgress();
            var bucket = $scope.userBuckets[index];

            bucketModel.addToBucket(bucket.id, art.id).then(function () {
                progress.hideProgress();
                close();
            }, function () {
                progress.hideProgress();
                alert.showAlert('Unable to add art to bucket');
            })
        };

        $scope.showCreateBucket = function () {
            bucketmodalService.showCreateBucket().then(function (result) {
                if (result && result.created) {
                    $scope.userBuckets.push(result.bucket);
                }
            });
        };

        $scope.close = function () {
            close();
        };
    }
]);