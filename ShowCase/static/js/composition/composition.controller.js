angular.module("CompositionApp").
controller("compositionController", [
	"$window",
	"$scope",
	"feedModel",
	"postModel",
	"contentManager",
	'$location',
	'$timeout',
	'analytics',
	'progress',
	'alert',
	'userModel',
    'bookService',
    'usermodalService',
    'bucketmodalService',
	function ($window,
		$scope,
		feedModel,
		postModel,
		contentManager,
		$location,
		$timeout,
		analytics,
		progress,
		alert,
		userModel,
        bookService,
        usermodalService,
        bucketmodalService)
	{

	$scope.composition = {};
	$scope.interpretations = [];
	$scope.hideName = true;
	$scope.interpretationModalshown = false;
    $scope.isBookMarked = false;

	$scope.init = function (id, url, slug, title, isBookMarked) {
		$scope.composition.id = id;
        $scope.composition.url = url;
        $scope.composition.slug = slug;
		$scope.composition.title = title;
        $scope.composition.is_bookMarked = isBookMarked == 'True';

		if (url) {
			analytics.logEvent('Composition', 'Init: ' + url);
		}
	};

	$scope.getNextPosts = function () {
		$scope.disableNextPost = true;
		var feed = $location.search()['feed'];
		var postId = $location.search()['post'];
		feedModel.nextPosts(feed, postId, $scope.composition.id).then(function (posts) {
			$scope.nextPosts = posts;
		});
	}();

    $scope.handleBookMark = function () {
    	var composition = $scope.composition;

        if (composition.is_bookMarked) {
            bookService.unmark(composition).then(function () {
            	composition.is_bookMarked = false;
            });
        } else {
            bookService.bookmark(composition).then(function () {
            	composition.is_bookMarked = true;
            });;
        }
    };

    $scope.showBookMarkers = function () {
        usermodalService.showBookMarkers($scope.composition).then(function (bookStatus) {
        	if (bookStatus == 'bookmarked') {
        		$scope.composition.is_bookMarked = true;
        	}
        });
    }

    $scope.showArtBuckets = function () {
        bucketmodalService.showArtBuckets($scope.composition);
    }

    $scope.showAddToBucket = function () {
        bucketmodalService.showAddToBucket($scope.composition);
    }
}])
.directive('postTemplate', [function () {
	return {
		restrict: 'A',
		scope: {
			'postData': '='
		},
		templateUrl: '/static/js/post/post.tpl.html',
		link: function (scope, element, attrs) {
			scope.post = scope.postData;
		}
	};
}])
.directive('toolsDrawer', [function () {
	return function (scope, element, attrs) {
		var open = false;
        var drawerControl = element.find('.drawer-control');
		drawerControl.bind('click', function () {
			if (open){
				element.removeClass('tools-extended');
			} else {
				element.addClass('tools-extended');
			}
			open = !open;
		})
	};
}]).directive('fitImage', function () {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
        	imagesLoaded(element, function () {
               imgElement = element[0]

                if (imgElement.width/$(window).width() > 0.8){
                    element.addClass('landscape');
                }
            })
        }
    }
});