angular.module('module.editArtModal')
.controller('editArtModalController', ['$scope',
    '$window',
    'art',
    'compositionModel',
    'bucketModel',
    'close',
    'progress',
    'alert',
    function ($scope, $window, art, compositionModel, bucketModel, close, progress, alert) {

        $scope.close = function () {
            close();
        };

        $scope.artistName = art.artist.name;
        $scope.art = art;
        $scope.art.artist = art.artist.id;
        $scope.uploadingDetails = false;

        function checkOrAddArtist () {
            if ($scope.art.artist === undefined || ((typeof($scope.art.artist) == 'string') && (JSON.parse($scope.art.artist).id == -1))){
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
            console.log($scope.art)
            // $scope.uploadingDetails = true;

            if (checkOrAddArtist()){

                compositionModel.updateArt($scope.art.slug, $scope.art).then(function (art) {
                    $window.location.href="/arts/" + art.slug;
                }, function () {
                    $scope.uploadingDetails = false;
                    alert.showAlert("Unable to update art info");
                })

            } else {
                $scope.uploadingDetails = false;
                progress.hideProgress();
                alert.showAlert("Please provide artist name");
            }
        }
    }
]);