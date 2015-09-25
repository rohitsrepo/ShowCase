angular.module('module.bucketmodal')
.controller('bucketmodalEditController', [
    '$scope',
    'bucketModel',
    'upload',
    'bucket',
    'close',
    'progress',
    'alert',
    function ($scope, bucketModel, upload, bucket, close, progress, alert) {

        $scope.bucket = bucket;
        $scope.editingBackground = false;
        var result = {edited: false};

        $scope.editBucket = function () {
            $scope.uploadingDetails = true;
            progress.showProgress();

            bucketModel.editBucket($scope.bucket).then(function (bucket) {
                progress.hideProgress();
                $scope.bucket = bucket;
                result.edited = true;
                result.bucket = bucket;
                $scope.uploadingDetails = false;
            }, function () {
                $scope.uploadingDetails = false;
                progress.hideProgress();
                alert.showAlert('Failed to edit series');
            });
        }

        $scope.toggleEditMode = function () {
            $scope.editingBackground = !$scope.editingBackground;
            $scope.loaded = true;
        };

        $scope.urlBackgroundUpload = function () {
            $scope.uploadingBackground = true;
            progress.showProgress();
            $scope.bucket.upload_type = 'url'

            bucketModel.updateBackground($scope.bucket.id, $scope.bucket).then(function (bucket) {
                $scope.bucket = bucket;
                result.bucket = bucket;
                result.edited = true;
                $scope.uploadingBackground = false;
                close(result);

                progress.hideProgress();
            } , function () {
                $scope.uploadingBackground = false;
                progress.hideProgress();
                alert.showAlert("Error fetching data for the image");
            })
        };

        $scope.uploadBackground = function (backgroundImageFile) {
            $scope.uploadingBackground = true;
            progress.showProgress();

            $scope.bucket.upload_type = 'upl'
            $scope.bucket.upload_image = backgroundImageFile

            upload({
                url: '/buckets/' + $scope.bucket.id + '/background',
                method: 'POST',
                data: $scope.bucket
            }).then(
                function (response) {
                    $scope.bucket = response.data;
                    result.bucket = response.data;
                    result.edited = true;
                    $scope.uploadingBackground = false;
                    close(result);

                    progress.hideProgress();
                },
                function (response) {
                    $scope.uploadingBackground = false;
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