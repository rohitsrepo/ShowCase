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

	var checkForScroll = function (interval) {
		$timeout (function () {
			var scrollTo = $location.search()['scrollTo'];
			if (scrollTo) {
				var elementTop = $('#'+scrollTo).offset().top;
				$('html,body').animate({
			        'scrollTop': elementTop
			    }, 750);
				analytics.logEvent('Composition', 'scroll-to: ' + scrollTo, $scope.composition.url);
			}
		}, interval);

	};

	$scope.$watch($scope.composition.Id, function () {
		postModel.getCompositionPosts($scope.composition.id).then(function (posts) {
			$scope.posts = posts;
			checkForScroll(500);
		});
	});

	$scope.isOutlineActive = "inactive";
	$scope.isGrayScaleActive = "inactive";

	$scope.showOutline = function () {
		if ($scope.isOutlineDisable && !$scope.isOutlineActive) {
			return;
		}

		analytics.logEvent('Composition', 'ToolBar - Outline: ' + $scope.isOutlineActive, $scope.composition.url);

		if($scope.isOutlineActive!="active"){
			$scope.isOutlineActive = '';
			$scope.isGrayScaleDisable = true;
			$timeout(function() {
				$scope.isOutlineActive = 'active';
			}, 600);
		} else {
			$scope.isOutlineActive = '';
			$scope.isGrayScaleDisable = false;
			$timeout(function() {
				$scope.isOutlineActive = 'inactive';
			}, 400);
		}
	};

	$scope.showGrayscale = function () {
		if ($scope.isGrayScaleDisable && !$scope.isGrayScaleActive) {
			return;
		}
		analytics.logEvent('Composition', 'ToolBar - GrayScale: ' + $scope.isGrayScaleActive, $scope.composition.url);

		if($scope.isGrayScaleActive!="active"){
			$scope.isGrayScaleActive = '';
			$scope.isOutlineDisable = true;
			$timeout(function() {
				$scope.isGrayScaleActive = 'active';
			}, 600);
		} else {
			$scope.isGrayScaleActive = '';
			$scope.isOutlineDisable = false;
			$timeout(function() {
				$scope.isGrayScaleActive = 'inactive';
			}, 400);
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