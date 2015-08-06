angular.module('ExploreApp')
.controller('exploreController', ['$scope', 'compositionModel', '$timeout', 'userModel', 'alert', 'progress', 'auth', 'modalService',
	function ($scope, compositionModel, $timeout, userModel, alert, progress, auth, modalService) {

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

	var bookmark = function (art) {
		auth.runWithAuth(function () {
			progress.showProgress();
			userModel.bookmark(art.id).then(function (response) {
				art.is_collected = true;
				progress.hideProgress();
			}, function () {
				progress.hideProgress();
				alert.showAlert('We are unable to process your response');
			});
		});
	}

	var unmark = function (art) {
		progress.showProgress();
		userModel.unmark(art.id).then(function (response) {
			art.is_collected = false;
			progress.hideProgress();
		}, function () {
			progress.hideProgress();
			alert.showAlert('We are unable to process your response');
		});
	};

    $scope.handleBookMark = function (index) {
        art = $scope.arts[index]
        if (art.is_collected) {
            unmark(art)
        } else {
            bookmark(art);
        }
    };


    $scope.showBookMarkers = function (index) {
        var art = $scope.arts[index];
        if (art.bookmarks_count == 0) {
            return;
        }

        modalService.showModal({
            'templateUrl': '/static/js/components/bookmark/bookmark.tpl.html',
            'controller': 'bookmarkController',
            'inputs' : {'composition': art}
        });
    };

}]);