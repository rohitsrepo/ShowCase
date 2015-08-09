angular.module('module.collectionmodal')
.controller('collectionmodalController', ['$scope',
    'compositionModel',
    'close',
    'art',
    'progress',
    'alert',
    function ($scope, compositionModel, close, art, progress, alert) {

        $scope.noSuchCollection = {
            status: false,
            action: function () {}
        }

        progress.showProgress();
        compositionModel.getCollections(art.id).then(function (collections) {
            $scope.collections = collections;

            if ($scope.collections.length == 0){
                $scope.noSuchCollection.status = true;
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