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

        $scope.bucketsLoaded = false;
        $scope.newMembership = {};
        $scope.gettingBuckets = true;
        $scope.addingDescription = false;

        $scope.art = art;
        bucketModel.myBuckets(art.id).then(function (buckets) {
            $scope.userBuckets = buckets;
            $scope.bucketsLoaded = true;

            if ($scope.userBuckets.length == 0){
                $scope.noUserBucket.status = true;
            }

            $scope.gettingBuckets = false;
        }, function () {
            alert.showAlert('We are unable to fetch data');
            $scope.gettingBuckets = false;
        });

        $scope.addToThisBucket = function (index) {
            var bucket = $scope.userBuckets[index];

            if (bucket.composition_added == true) {
                alert.showAlert("Artwork is already present in this series")
                return;
            }

            $scope.addingDescription = true;
            $scope.newMembership.bucket = bucket;
        }

        $scope.completeAddToBucket = function (description) {

            if (addingCount) {
                addingCount++;
            } else {
                $scope.addingToBucket = true;
            }

            bucketModel.addToBucket($scope.newMembership.bucket.id,
                art.id,
                description)
            .then(function () {

                if (addingCount) {
                    addingCount--;
                } else {
                    $scope.addingToBucket = false;
                }

                $scope.newMembership.bucket.composition_added = true;
                $scope.addingDescription = false;
                $scope.newMembership.description = '';
                $scope.newMembership.index = '';
                $scope.close();
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