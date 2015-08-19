angular.module('module.bucketmodal')
.controller('bucketmodalCreateController', [
    '$scope',
    'bucketModel',
    'upload',
    'close',
    'progress',
    'alert',
    function ($scope, bucketModel, upload, close, progress, alert) {

        $scope.newBucket = {};
        $scope.bucketCreated = false;
        var result = {};

        $scope.createNewBucket = function () {
            progress.showProgress();

            bucketModel.create($scope.newBucket).then(function (bucket) {
                progress.hideProgress();

                result = {
                    'created': true,
                    'bucket': bucket
                }

                $scope.bucketCreated = true;
            }, function () {
                progress.hideProgress();
                alert.showAlert('Unable to create new series');
            });
        }

        $scope.urlBackgroundUpload = function () {
            progress.showProgress()
            $scope.newBucket.upload_type = 'url'

            bucketModel.updateBackground(result.bucket.id, $scope.newBucket).then(function (bucket) {
                result.bucket = bucket
                close(result);

                progress.hideProgress();
            } , function () {
                progress.hideProgress();
                alert.showAlert("Error fetching data for the image");
            })
        };

        $scope.uploadBackground = function (backgroundImageFile) {
            progress.showProgress();

            $scope.newBucket.upload_type = 'upl'
            $scope.newBucket.upload_image = backgroundImageFile

            upload({
                url: '/buckets/' + result.bucket.id + '/background',
                method: 'POST',
                data: $scope.newBucket
            }).then(
                function (response) {
                    result.bucket = response.data;
                    close(result);

                    progress.hideProgress();
                },
                function (response) {
                    progress.hideProgress();
                    alert.showAlert('Unable to upload image');
                }
            );
        };

        $scope.close = function () {
            close(result);
        };
    }
])
.directive("bucketFileread", [function () {
    return  function (scope, element, attributes) {
            element.bind("change", function (changeEvent) {
                scope.$apply(function () {
                    var backgroundImageFile = changeEvent.target.files[0];
                    scope.uploadBackground(backgroundImageFile);
                });
            });
        }
}]);;