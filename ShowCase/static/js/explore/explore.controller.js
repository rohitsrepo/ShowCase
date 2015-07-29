angular.module('ExploreApp')
.controller('exploreController', ['$scope', 'compositionModel', '$timeout', 'userModel', 'alert', 'progress', 'auth',
	function ($scope, compositionModel, $timeout, userModel, alert, progress, auth) {

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

	$scope.loadMoreArts();

	$scope.addToCollection = function (index) {
		auth.runWithAuth(function () {
			art = $scope.arts[index]
			progress.showProgress();
			userModel.addToCollection(art.id).then(function (response) {
				$scope.arts[index].is_collected = true;
				progress.hideProgress();
			}, function () {
				progress.hideProgress();
				alert.showAlert('We are unable to process your response');
			});
		});
	}

	$scope.removeFromCollection = function (index) {
		art = $scope.arts[index]
		progress.showProgress();
		userModel.removeFromCollection(art.id).then(function (response) {
			$scope.arts[index].is_collected = false;
			progress.hideProgress();
		}, function () {
			progress.hideProgress();
			alert.showAlert('We are unable to process your response');
		});
	};

}]);