angular.module('module.seriesmodal')
.controller('seriesmodalController', ['$scope',
    'compositionModel',
    'close',
    'art',
    'progress',
    'alert',
    function ($scope, compositionModel, close, art, progress, alert) {

        $scope.noSuchSeries = {
            status: false,
            action: function () {}
        }

        progress.showProgress();
        compositionModel.getSerieses(art.id).then(function (serieses) {
            $scope.serieses = serieses;

            if ($scope.serieses.length == 0){
                $scope.noSuchSeries.status = true;
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