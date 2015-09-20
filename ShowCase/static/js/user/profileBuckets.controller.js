angular.module('UserApp')
.controller('profileBucketsController', ['$scope',
    'bucketModel',
    'bucketmodalService',
    'followBucketService',
    'shareModalService',
    'progress',
    'alert',
    function ($scope, bucketModel, bucketmodalService, followBucketService, shareModalService, progress, alert) {

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
    };

    $scope.shareBucket = function (event, index) {
        // Stop route change on click
        event.stopPropagation();

        var bucket = $scope.userBuckets[index];
        var base_url = "http://thirddime.com";
        var share_url = base_url + "/@" + bucket.owner.slug + '/series/' + bucket.slug;
        var title = 'Series: "' + bucket.name + '" by: ' + bucket.owner.name;
        var description = bucket.description + '...Complete series can be found at: ' + share_url;
        var media = 'http://thirddime.com' + bucket.picture;
        shareModalService.shareThisPage(share_url, title, description, media);
    };

    $scope.watchBucket = function (event, index) {
        // Stop route change on click
        event.stopPropagation();

        var bucket = $scope.userBuckets[index];
        followBucketService.watchBucket(bucket.id).then(function () {
            bucket.is_watched = true;
        });
    };

    $scope.unwatchBucket = function (event, index) {
        // Stop route change on click
        event.stopPropagation();

        var bucket = $scope.userBuckets[index];
        followBucketService.unwatchBucket(bucket.id).then(function () {
            bucket.is_watched = false;
        });
    };

}]);