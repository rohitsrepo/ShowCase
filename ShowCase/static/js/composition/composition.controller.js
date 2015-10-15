angular.module("CompositionApp").
controller("compositionController", [
	"$window",
    '$document',
	"$scope",
    '$rootScope',
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
    'admireService',
    'usermodalService',
    'bucketmodalService',
    'compositionModel',
    'shareModalService',
	function ($window,
        $document,
        $scope,
        $rootScope,
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
        admireService,
        usermodalService,
        bucketmodalService,
        compositionModel,
        shareModalService)
	{

	$scope.composition = {};
	$scope.interpretations = [];
	$scope.hideName = true;
	$scope.interpretationModalshown = false;
    $scope.isBookMarked = false;

    // Disable scroll on parent page
    $rootScope.$on('$stateChangeSuccess',
    function(event, toState, toParams, fromState, fromParams){
        var body = $document.find('body');
        body.addClass('modal-open');

        if (toState.name == 'art') {
            body.removeClass('modal-open');
        }
    });

    var getArtAssociates = function () {
        compositionModel.getAssociates($scope.composition.id).then(function (response) {
            $scope.artBuckets = response.artBuckets;
            $scope.artistWorks = response.artistWorks;
            $scope.uploaderWorks = response.uploaderWorks;
        });
    };

	$scope.init = function (id, url, matter_550, slug, title, artist, isBookMarked, is_admired) {
		$scope.composition.id = id;
        $scope.composition.url = url;
        $scope.composition.matter = url;
        $scope.composition.matter_550 = matter_550;
        $scope.composition.slug = slug;
        $scope.composition.title = title;
		$scope.composition.artist = artist;
        $scope.composition.is_bookMarked = isBookMarked == 'True';
        $scope.composition.is_admired = is_admired == 'True';

		if (url) {
			analytics.logEvent('Composition', 'Init: ' + url);
		}

        getArtAssociates(id);
	};

    $scope.handleBookMark = function () {
    	var composition = $scope.composition;

        if (composition.is_bookMarked) {
            bookService.unmarkArt(composition).then(function () {
            	composition.is_bookMarked = false;
            });
        } else {
            bookService.bookmarkArt(composition).then(function () {
            	composition.is_bookMarked = true;
            });;
        }
    };

    $scope.handleAdmire = function () {
        var art = $scope.composition;

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

    $scope.showBookMarkers = function () {
        usermodalService.showBookMarkers($scope.composition).then(function (bookStatus) {
            if (bookStatus == 'bookmarked') {
                $scope.composition.is_bookMarked = true;
            }
        });
    }

    $scope.showAdmirers = function () {
        usermodalService.showArtAdmirers($scope.composition).then(function (admireStatus) {
            if (admireStatus == 'admired') {
                $scope.composition.is_admired = true;
            }
        });
    }

    $scope.showArtBuckets = function () {
        bucketmodalService.showArtBuckets($scope.composition);
    }

    $scope.showAddToBucket = function (event, art) {
        event.stopPropagation();
        bucketmodalService.showAddToBucket(art);
    }

    $scope.showShare = function () {
        var share_url = window.location.href;
        var title = 'Artwork: "' + $scope.composition.title + '" by: ' + $scope.composition.artist;
        var description = 'Find thoughts about artwork "' + $scope.composition.title+
            '" at ' + share_url;
        var media = 'http://thirddime.com' + $scope.composition.url;
        shareModalService.shareThisPage(share_url, title, description, media);
    };

    $scope.shareArt = function (event, art) {
        event.stopPropagation();

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

        var bucket = $scope.artBuckets[index];
        var base_url = "http://thirddime.com";
        var share_url = base_url + "/@" + bucket.owner.slug + '/series/' + bucket.slug;
        var title = 'Series: "' + bucket.name + '" by: ' + bucket.owner.name;
        var description = bucket.description + '...Complete series can be found at: ' + share_url;
        var media = 'http://thirddime.com' + bucket.picture;
        shareModalService.shareThisPage(share_url, title, description, media);
    };

    $scope.handleBookMarkArt = function (event, art) {
        event.stopPropagation();

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

    $scope.handleAdmireArt = function (event, art) {
        event.stopPropagation();

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

        var bucket = $scope.artBuckets[index];
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

        var bucket = $scope.artBuckets[index];
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