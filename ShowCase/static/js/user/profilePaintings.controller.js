angular.module('UserApp')
.controller('profilePaintingsController', ['$scope', 'userModel', 'progress', 'alert', function ($scope, userModel, progress, alert) {
    $scope.compositions = [];
    $scope.compositionsMeta = {pageVal: 1, disableGetMore: false, busy: false, next:'', previous:'', noWorks: false};

    var getCompositions = function () {

        if (!$scope.compositionsMeta.disableGetMore) {
            var pageVal = $scope.compositionsMeta.pageVal;
            progress.showProgress();
            userModel.getCompositions($scope.artist.id, pageVal).then(function (response) {
                $scope.compositionsMeta.next = response.next;
                $scope.compositionsMeta.previous = response.previous;

                for (var i = 0; i < response.results.length; i++) {
                    $scope.compositions.push(response.results[i]);
                }

                if (response.next == null){
                    $scope.compositionsMeta.disableGetMore = true;
                }
                    console.log('settion it to false', $scope.compositions.length);

                if ($scope.compositions.length == 0){
                    console.log('settion it to false');
                    $scope.compositionsMeta.noWorks = true;
                }

                progress.hideProgress();
                $scope.compositionsMeta.busy = false;
            }, function () {
                alert.showAlert('We are facing some problems fetching data');
                progress.hideProgress();
            });
        }

        $scope.compositionsMeta.pageVal += 1;
    };

    $scope.loadMoreCompositions = function () {
        if ($scope.compositionsMeta.busy) {
            return;
        }

        $scope.compositionsMeta.busy = true;
        getCompositions();
    }

}]);