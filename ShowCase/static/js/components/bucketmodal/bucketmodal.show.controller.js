angular.module('module.bucketmodal')
.controller('bucketmodalShowController', ['$scope',
    'bucketModel',
    'close',
    'art',
    'progress',
    'alert',
    function ($scope, bucketModel, close, art, progress, alert) {

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

        $scope.close = function () {
            close();
        };
    }
]);