angular.module('UserApp')
.controller('profileBucketsController', ['$scope',
    'bucketModel',
    'bucketmodalService',
    'progress',
    'alert',
    function ($scope, bucketModel, bucketmodalService, progress, alert) {

    $scope.noSuchBucket = {
        status: false,
        action: function () {}
    }

    progress.showProgress();
    bucketModel.userBuckets($scope.artist.id).then(function (buckets) {
        $scope.userBuckets = buckets;

        if ($scope.userBuckets.length == 0){
            $scope.noSuchBucket.status = true;
        }

        progress.hideProgress();
    }, function () {
        alert.showAlert('We are unable to fetch data');
        progress.hideProgress();
    });

    $scope.showArts = function (index) {
        var bucket = $scope.userBuckets[index];
        bucketmodalService.showBucketArts(bucket);
    }

}]);