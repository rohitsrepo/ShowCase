angular.module('module.uploadmodal')
.controller('uploadmodalController', ['$scope',
    '$window',
    'compositionModel',
    'bucketModel',
    'upload',
    'user',
    'close',
    'progress',
    'alert',
    function ($scope, $window, compositionModel, bucketModel, upload, user, close, progress, alert) {

        $scope.close = function () {
            close();
        };

        $scope.art = {};
        $scope.imageUploaded = false;

        var showInfoForm = function (imageData) {
            $scope.artImage = imageData;
            $scope.imageUploaded = true;

            // Load user buckets
            bucketModel.userBuckets(user.id).then(function (buckets) {
                $scope.userBuckets = buckets;
            });
        };

        $scope.uploadArt = function (artImageFile) {
            progress.showProgress();

            $scope.art.upload_type = 'upl'
            $scope.art.upload_image = artImageFile

            upload({
                url: '/compositions/matter',
                method: 'POST',
                data: $scope.art
            }).then(
                function (response) {
                    showInfoForm(response.data);
                    progress.hideProgress();
                },
                function (response) {
                    progress.hideProgress();
                    alert.showAlert('Unable to upload image');
                }
            );
        };

        $scope.urlUpload = function () {
            progress.showProgress()
            $scope.art.upload_type = 'url'

            compositionModel.urlImageUploader($scope.art).then(function (response) {
                showInfoForm(response);
                progress.hideProgress();
            } , function () {
                progress.hideProgress();
                alert.showAlert("Error fetching data for the image");
            })
        }

        function checkOrAddArtist () {
            if ($scope.art.artist === undefined || JSON.parse($scope.art.artist).id == -1){
                var artistName = $('.artist-input')[0].value;
                if (artistName === '') {
                    return false;
                }

                $scope.art.artist = JSON.stringify({'id': -1,'name': artistName})
            }

            return true;
        }

        $scope.selectArtist = function (selectedArtist) {
            if (selectedArtist === undefined){
                $scope.art.artist = JSON.stringify({'id': -1,'name': $('.artist-input')[0].val})
            } else {
                $scope.art.artist = selectedArtist.originalObject.id;
            }
        }

        $scope.submitArtInfo = function () {
            progress.showProgress();

            if (checkOrAddArtist()){
                $scope.art.image_id = $scope.artImage.id;

                compositionModel.addArt($scope.art).then(function (art) {
                    progress.hideProgress();
                    $window.location.href="/arts/" + art.slug;
                }, function () {
                    progress.hideProgress();
                    alert.showAlert("Unable to update art info");
                })

            } else {
                progress.hideProgress();
                alert.showAlert("Please provide artist name");
            }
        }
    }
])
.directive("fileread", [function () {
    return  function (scope, element, attributes) {
            element.bind("change", function (changeEvent) {
                scope.$apply(function () {
                    var artImageFile = changeEvent.target.files[0];
                    scope.uploadArt(artImageFile);
                });
            });
        }
}]);