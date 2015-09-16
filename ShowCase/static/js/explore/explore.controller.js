angular.module('ExploreApp')
.controller('exploreController', ['$scope',
    '$rootScope',
    '$document',
    'feedModel',
    '$timeout',
    'userModel',
    'alert',
    'progress',
    'auth',
    'bookService',
    'bucketmodalService',
    'usermodalService',
	function ($scope, $rootScope, $document, feedModel, $timeout, userModel, alert, progress, auth, bookService, bucketmodalService, usermodalService) {

    $scope.math = window.Math
	$scope.arts = [];
	$scope.postsMeta = {pageVal: 1, disableGetMore: false, busy: false, next:'', previous:'', feedType:'fresh'};

    var getPostFetcher = function () {
        if ($scope.postsMeta.feedType === 'fresh') {
            return feedModel.getFresh;
        } else if ($scope.postsMeta.feedType === 'staff') {
            return feedModel.getStaff;
        }
    };

    // Disable scroll on parent page
    $rootScope.$on('$stateChangeSuccess',
    function(event, toState, toParams, fromState, fromParams){
        var body = $document.find('body');
        if (fromState.name == 'arts') {
            body.addClass('modal-open');
        } else if (toState.name == 'arts') {
            body.removeClass('modal-open');
        }
    });

	var getPosts = function () {

	    if (!$scope.postsMeta.disableGetMore) {
            progress.showProgress();

	        var pageVal = $scope.postsMeta.pageVal;
	        getPostFetcher()(pageVal).then(function (response) {
	            $scope.postsMeta.next = response.next;
	            $scope.postsMeta.previous = response.previous;

	            for (var i = 0; i < response.results.length; i++) {
	                $scope.arts.push(response.results[i]);
	            }

	            if (response.next == null){
	                $scope.postsMeta.disableGetMore = true;
	            }

	            $timeout(function () {
    			    $scope.postsMeta.pageVal += 1;
    	            $scope.postsMeta.busy = false;
	            }, 500);

                progress.hideProgress();

	        });
	    }

	};

	$scope.loadMorePosts = function () {
	    if ($scope.postsMeta.busy) {
	        return;
	    }

	    $scope.postsMeta.busy = true;
	    getPosts();
	}

	$scope.loadMorePosts();

    $scope.switchPostSource = function (feedType) {
        if (feedType !== $scope.postsMeta.feedType) {
            $scope.postsMeta.disableGetMore = true;

            $scope.postsMeta = {
                pageVal: 1,
                busy: false,
                next:'',
                previous:'',
                feedType:feedType
            };

            $scope.arts = [];
            $scope.postsMeta.disableGetMore = false;
            getPosts();
        }
    };

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

    $scope.showArtBuckets = function (index) {
        var art = $scope.arts[index];
        bucketmodalService.showArtBuckets(art);
    }

    $scope.showAddToBucket = function (index) {
        var art = $scope.arts[index];
        bucketmodalService.showAddToBucket(art);
    };

    $scope.toggleNsfw = function (index) {
        var art = $scope.arts[index];
        art.nsfw = false;
    }

}]);