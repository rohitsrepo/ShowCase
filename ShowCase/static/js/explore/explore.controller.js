angular.module('ExploreApp')
.controller('exploreController', ['$scope', 'compositionModel', '$timeout', function ($scope, compositionModel, $timeout) {

	$scope.arts = [];
	$scope.artsMeta = {pageVal: 1, disableGetMore: false, busy: false, next:'', previous:''};

	var getArts = function () {

	    if (!$scope.artsMeta.disableGetMore) {
	        var pageVal = $scope.artsMeta.pageVal;
	        compositionModel.getExplores(pageVal).then(function (response) {
	            $scope.artsMeta.next = response.next;
	            $scope.artsMeta.previous = response.previous;

	            for (var i = 0; i < response.results.length; i++) {
	                $scope.arts.push(response.results[i]);
	            }

	            if (response.next == null){
	                $scope.artsMeta.disableGetMore = true;
	            }

	            $timeout(function () {
    			    $scope.artsMeta.pageVal += 1;
    	            $scope.artsMeta.busy = false;
	            }, 500);

	        });
	    }

	};

	$scope.loadMoreArts = function () {
	    if ($scope.artsMeta.busy) {
	        return;
	    }

	    $scope.artsMeta.busy = true;
	    getArts();
	}

}]);