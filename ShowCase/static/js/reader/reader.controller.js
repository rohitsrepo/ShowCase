angular.module("ReaderApp")
.controller("readerController", ["$scope",
    'bucketModel',
    'bucketmodalService',
    function ($scope, bucketModel, bucketmodalService)
 {
	"use strict";

    $scope.readerBuckets = []
    var buckets = ['through-dull-glass', 'dance-of-light', 'children-of-war']

    var getBuckets = function () {
        angular.forEach(buckets, function (value) {
            bucketModel.getBucket(value).then(function (response) {
                $scope.readerBuckets.push(response);
            });
        });
    }();

    $scope.showSeries = function (index) {
        var bucket = $scope.readerBuckets[index];
        bucketmodalService.showBucketArts(bucket);
    };

}]);