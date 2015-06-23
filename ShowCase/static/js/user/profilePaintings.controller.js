angular.module('UserApp')
.controller('profilePaintingsController', ['$scope', 'userModel', function ($scope, userModel) {
    $scope.compositions = [];
    $scope.compositionsMeta = {pageVal: 1, disableGetMore: false, busy: false, next:'', previous:''};

    var getCompositions = function () {

        if (!$scope.compositionsMeta.disableGetMore) {
            var pageVal = $scope.compositionsMeta.pageVal;
            userModel.getCompositions($scope.artist.id, pageVal).then(function (response) {
                $scope.compositionsMeta.next = response.next;
                $scope.compositionsMeta.previous = response.previous;

                for (var i = 0; i < response.results.length; i++) {
                    $scope.compositions.push(response.results[i]);
                }

                if (response.next == null){
                    $scope.compositionsMeta.disableGetMore = true;
                }

                $scope.compositionsMeta.busy = false;
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