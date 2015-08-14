angular.module('module.bucketmodal')
.controller('bucketmodalContentController', ['$scope',
    'bucketModel',
    'bucketmodalService',
    'close',
    'bucket',
    'progress',
    'alert',
    function ($scope, bucketModel, bucketmodalService, close, bucket, progress, alert) {

        progress.showProgress();
        $scope.bucket = bucket;

        bucketModel.bucketArts(bucket.id).then(function (arts) {
            $scope.bucketArts = arts;
            progress.hideProgress();
        }, function () {
            alert.showAlert('We are unable to art for this series');
            progress.hideProgress();
        });

        $scope.close = function () {
            close();
        };
    }
]);