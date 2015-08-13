angular.module('module.bucketmodal')
.controller('bucketmodalCreateController', [
    '$scope',
    'bucketModel',
    'close',
    'progress',
    'alert',
    function ($scope, bucketModel, close, progress, alert) {

        $scope.newBucket = {};

        $scope.createNewBucket = function () {
            progress.showProgress();

            bucketModel.create($scope.newBucket).then(function (bucket) {
                progress.hideProgress();

                var result = {
                    'created': true,
                    'bucket': bucket
                }

                close(result);

            }, function () {
                progress.hideProgress();
                alert.showAlert('Unable to create new series');
            });
        }

        $scope.close = function () {
            close();
        };
    }
]);