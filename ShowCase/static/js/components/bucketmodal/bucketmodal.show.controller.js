angular.module('module.bucketmodal')
.controller('bucketmodalShowController', ['$scope',
    'bucketModel',
    'bucketmodalService',
    'close',
    'art',
    'progress',
    'alert',
    function ($scope, bucketModel, bucketmodalService, close, art, progress, alert) {

        $scope.noSuchBucket = {
            status: false,
            action: function () {}
        }

        progress.showProgress();
        $scope.art = art;
        bucketModel.artBuckets(art.id).then(function (buckets) {
            $scope.artBuckets = buckets;

            if ($scope.artBuckets.length == 0){
                $scope.noSuchBucket.status = true;
            }

            progress.hideProgress();
        }, function () {
            alert.showAlert('We are unable to fetch data');
            progress.hideProgress();
        });

        $scope.showArts = function (index) {
            var bucket = $scope.artBuckets[index];
            bucketmodalService.showBucketArts(bucket);
        }

        $scope.close = function () {
            close();
        };
    }
]);