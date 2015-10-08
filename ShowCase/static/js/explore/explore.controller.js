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
    'admireService',
    'bucketmodalService',
    'usermodalService',
    'shareModalService',
	function ($scope,
        $rootScope,
        $document,
        feedModel,
        $timeout,
        userModel,
        alert,
        progress,
        auth,
        bookService,
        admireService,
        bucketmodalService,
        usermodalService,
        shareModalService) {

    $scope.math = window.Math
	$scope.arts = [];
	$scope.postsMeta = {pageVal: 1, disableGetMore: false, busy: false, next:'', previous:'', feedType:'staff'};

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
        var art = $scope.arts[index].content;
        if (art.is_bookmarked) {
            bookService.unmarkArt(art).then(function () {
                art.is_bookmarked = false;
            });
        } else {
            bookService.bookmarkArt(art).then(function () {
                art.is_bookmarked = true;
            });;
        }
    };

    $scope.handleAdmireArt = function (index) {
        var art = $scope.arts[index].content;
        if (art.is_admired) {
            admireService.unadmireArt(art).then(function () {
                art.is_admired = false;
            });
        } else {
            admireService.admireArt(art).then(function () {
                art.is_admired = true;
            });;
        }
    };

    $scope.handleBookMarkBucket = function (event, index) {
        event.stopPropagation();

        var bucket = $scope.arts[index].content;
        if (bucket.is_bookmarked) {
            bookService.unmarkBucket(bucket).then(function () {
                bucket.is_bookmarked = false;
            });
        } else {
            bookService.bookmarkBucket(bucket).then(function () {
                bucket.is_bookmarked = true;
            });;
        }
    };

    $scope.handleAdmireBucket = function (event, index) {
        event.stopPropagation();

        var bucket = $scope.arts[index].content;
        if (bucket.is_admired) {
            admireService.unadmireBucket(bucket).then(function () {
                bucket.is_admired = false;
            });
        } else {
            admireService.admireBucket(bucket).then(function () {
                bucket.is_admired = true;
            });;
        }
    };

    $scope.showArtBuckets = function (index) {
        var art = $scope.arts[index].content;
        bucketmodalService.showArtBuckets(art);
    }

    $scope.showAddToBucket = function (index) {
        var art = $scope.arts[index].content;
        bucketmodalService.showAddToBucket(art);
    };

    $scope.toggleNsfw = function (index) {
        var art = $scope.arts[index].content;
        art.nsfw = false;
    };

    $scope.shareArt = function (index) {
        var art = $scope.arts[index].content;
        var base_url = "http://thirddime.com";
        var share_url = base_url + "/arts/" + art.slug;
        var title = 'Artwork: "' + art.title + '" by: ' + art.artist.name;
        var description = 'Find thoughts about artwork "' + art.title+
            '" at ' + share_url;
        var media = 'http://thirddime.com' + art.matter;
        shareModalService.shareThisPage(share_url, title, description, media);
    };

    $scope.shareBucket = function (event, index) {
        // Stop route change on click
        event.stopPropagation();

        var bucket = $scope.arts[index].content;
        var base_url = "http://thirddime.com";
        var share_url = base_url + "/@" + bucket.owner.slug + '/series/' + bucket.slug;
        var title = 'Series: "' + bucket.name + '" by: ' + bucket.owner.name;
        var description = bucket.description + '...Complete series can be found at: ' + share_url;
        var media = 'http://thirddime.com' + bucket.picture;
        shareModalService.shareThisPage(share_url, title, description, media);
    };

}]);