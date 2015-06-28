angular.module('UserApp')
.controller('profileInterpretationsController', ['$scope', 'userModel', function ($scope, userModel) {
    $scope.interpretationsMeta = {pageVal: 1, disableGetMore: false, busy: false, next:'', previous:''};
    $scope.interpretations = [];

    var getInterpretations = function () {

        if (!$scope.interpretationsMeta.disableGetMore) {
            var pageVal = $scope.interpretationsMeta.pageVal;
            userModel.getInterpretations($scope.artist.id, pageVal).then(function (interpretations) {
                $scope.interpretationsMeta.next = interpretations.next;
                $scope.interpretationsMeta.previous = interpretations.previous;

                for (var i = 0; i < interpretations.results.length; i++) {
                    $scope.interpretations.push(interpretations.results[i]);
                }

                if (interpretations.next == null){
                    $scope.interpretationsMeta.disableGetMore = true;
                    // analytics.logEvent('Reader', 'Load More interpretations - Hit Bottom');
                }

                $scope.interpretationsMeta.busy = false;
            });
        }

        $scope.interpretationsMeta.pageVal += 1;
    }

    $scope.loadMoreInterpretations = function () {
        if ($scope.interpretationsMeta.busy) {
            return;
        }

        $scope.interpretationsMeta.busy = true;
        if ($scope.interpretations.length != 0){
            // analytics.logEvent('Reader', 'Load More interpretations');
        } else {
            // analytics.logEvent('Reader', 'Init');
        }
        getInterpretations();
    };



}]);