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
        var addingCount = 0;

        $scope.showCreateBucket = function () {
            bucketmodalService.showCreateBucket().then(function (result) {
                if (result && result.created) {
                    $scope.userBuckets.unshift(result.bucket);
                    $scope.noUserBucket.status = false;
                }
            });
        };

        $scope.noUserBucket = {
            status: false,
            action: function () {
                $scope.showCreateBucket();
            }
        }

        $scope.gettingBuckets = true;
        $scope.art = art;
        bucketModel.userBuckets(user.id, art.id).then(function (buckets) {
            $scope.userBuckets = buckets;

            if ($scope.userBuckets.length == 0){
                $scope.noUserBucket.status = true;
            }

            $scope.gettingBuckets = false;
        }, function () {
            alert.showAlert('We are unable to fetch data');
            $scope.gettingBuckets = false;
        });

        $scope.addToThisBucket = function (index) {
            if (addingCount) {
                addingCount++;
            } else {
                $scope.addingToBucket = true;
            }

            var bucket = $scope.userBuckets[index];

            bucketModel.addToBucket(bucket.id, art.id).then(function () {
                if (addingCount) {
                    addingCount--;
                } else {
                    $scope.addingToBucket = false;
                }

                bucket.composition_added = true;
            }, function () {
                if (addingCount) {
                    addingCount--;
                } else {
                    $scope.addingToBucket = false;
                }

                alert.showAlert('Unable to add art to bucket');
            })
        };

        $scope.close = function () {
            close();
        };
    }
]);