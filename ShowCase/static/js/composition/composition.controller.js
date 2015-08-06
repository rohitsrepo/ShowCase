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
    'modalService',
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
        modalService)
	{

	$scope.composition = {};
	$scope.interpretations = [];
	$scope.hideName = true;
	$scope.interpretationModalshown = false;
    $scope.isBookMarked = false;

	$scope.init = function (id, url, isBookMarked) {
		$scope.composition.id = id;
		$scope.composition.url = url;
        $scope.isBookMarked = isBookMarked == 'True';

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

	var bookmark = function () {
		progress.showProgress();
		userModel.bookmark($scope.composition.id).then(function (response) {
            $scope.isBookMarked = true;
			progress.hideProgress();
		}, function () {
			progress.hideProgress();
			alert.showAlert('We are unable to process your response');
		});
	};

	var unmark = function () {
		progress.showProgress();
		userModel.unmark($scope.composition.id).then(function (response) {
            $scope.isBookMarked = false;
			progress.hideProgress();
		}, function () {
			progress.hideProgress();
			alert.showAlert('We are unable to process your response');
		});
	};

    $scope.handleBookMark = function () {
        if ($scope.isBookMarked) {
            unmark();
        } else {
            bookmark();
        }
    };

    $scope.showBookMarkers = function () {
        modalService.showModal({
            'templateUrl': '/static/js/components/bookmark/bookmark.tpl.html',
            'controller': 'bookmarkController',
            'inputs' : {'composition': $scope.composition}
        });
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
		element.bind('click', function () {
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