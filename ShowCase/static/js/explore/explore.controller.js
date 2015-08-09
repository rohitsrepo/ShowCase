angular.module('ExploreApp')
.controller('exploreController', ['$scope',
    'compositionModel',
    '$timeout',
    'userModel',
    'alert',
    'progress',
    'auth',
    'bookService',
    'collectionmodalService',
    'usermodalService',
	function ($scope, compositionModel, $timeout, userModel, alert, progress, auth, bookService, collectionmodalService, usermodalService) {

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

    $scope.handleBookMark = function (index) {
        art = $scope.arts[index]
        if (art.is_bookmarked) {
            bookService.unmark(art).then(function () {
            	art.is_bookmarked = false;
            });
        } else {
            bookService.bookmark(art).then(function () {
            	art.is_bookmarked = true;
            });;
        }
    };

    $scope.showBookMarkers = function (index) {
        var art = $scope.arts[index];

        usermodalService.showBookMarkers(art).then(function (bookStatus) {
        	if (bookStatus == 'bookmarked') {
        		art.is_bookmarked = true;
        	}
        });
    };

    $scope.showCollections = function (index) {
        var art = $scope.arts[index];
        collectionmodalService.showCollections(art);
    }

}]);