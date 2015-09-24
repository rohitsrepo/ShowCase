angular.module('module.bucketmodal')
.controller('bucketmodalContentController', ['$scope',
    '$window',
    '$state',
    'auth',
    'bucketModel',
    'bucketmodalService',
    'confirmModalService',
    'shareModalService',
    'close',
    'bucket',
    'progress',
    'alert',
    function ($scope, $window, $state, auth, bucketModel, bucketmodalService, confirmModalService, shareModalService, close, bucket, progress, alert) {

        progress.showProgress();
        $scope.bucket = bucket;
        $scope.noArts = false;
        $scope.math = window.Math;
        $scope.isState = $state.current.data && $state.current.data.isState;
        var currentShowIndex = 0;

        bucketModel.bucketArts(bucket.id).then(function (arts) {
            if (arts.length > 0){
                $scope.bucketArts = arts;
                $scope.bucketArts[currentShowIndex].show = true;
            } else {
                $scope.noArts = true;
            }

            progress.hideProgress();
        }, function () {
            alert.showAlert('We are currently unable to get art for this series');
            progress.hideProgress();
        });


        $scope.toggleNsfw = function (index) {
            var art = $scope.bucketArts[index];
            art.nsfw = false;
        }

        $scope.nextArt = function () {

            if ($scope.bucketArts.length > currentShowIndex + 1){
                $scope.bucketArts[currentShowIndex].show = false;
                currentShowIndex = currentShowIndex + 1;
                $scope.bucketArts[currentShowIndex].show = true;
            }
        }

        $scope.prevArt = function () {

            if (currentShowIndex > 0){
                $scope.bucketArts[currentShowIndex].show = false;
                currentShowIndex = currentShowIndex - 1;
                $scope.bucketArts[currentShowIndex].show = true;
            }
        }

        $scope.back = function () {
            if ($scope.isState){
                $window.history.back();
            } else {
                $scope.close();
            }
        };

        $scope.close = function () {
            close();
        };

        $scope.watchBucket = function () {
            followBucketService.watchBucket($scope.bucket.id).then(function () {
                $scope.bucket.is_watched = true;
            });
        };

        $scope.unwatchBucket = function () {
            followBucketService.unwatchBucket($scope.bucket.id).then(function () {
                $scope.bucket.is_watched = false;
            });
        };

        $scope.removeFromBucket = function (index) {
            progress.hideProgress();
            var art = $scope.bucketArts[index];

            confirmModalService.showDeleteConfirm().then(function () {
                bucketModel.removeFromBucket($scope.bucket.id, art.id).then(function () {
                    $scope.removeFromSly(index);
                    $scope.bucketArts.splice(index, 1);
                    progress.hideProgress();
                }, function () {
                    progress.hideProgress();
                    alert.showAlert('Currently unable to remove this art from the series');
                });
            });
        };

        $scope.deleteBucket = function () {
            progress.showProgress();

            confirmModalService.showDeleteConfirm().then(function () {
                bucketModel.deleteBucket($scope.bucket.slug).then(function () {
                    window.location.href = '/@' + bucket.owner.slug + '/series';
                }, function () {
                    progress.hideProgress();
                    alert.showAlert('Currently unable to delete this series');
                });
            });
        };

        $scope.showEditBucket = function () {
            bucketmodalService.showEditBucket($scope.bucket).then(function (bucket) {
                window.location.href = "/@" + bucket.owner.slug + '/series/' + bucket.slug;
            });
        };

        $scope.showShare = function () {
            var base_url = 'http://thirddime.com';
            var share_url = base_url + '/@' + $scope.bucket.owner.slug + '/series/' + $scope.bucket.slug;
            var title = 'Series: "' + $scope.bucket.name + '" by: ' + $scope.bucket.owner.name;
            var description = $scope.bucket.description + '...Complete series can be found at: ' + share_url;
            var media = base_url + $scope.bucket.picture;
            shareModalService.shareThisPage(share_url, title, description, media);
        };

    }
])
.directive('keyEventBinderContent', ['$window', function ($window) {
    return function (scope, element, attrs) {
        element.focus();
        element.bind('keydown', function (evt) {

            if (evt.keyCode == 27) {
                if (scope.isState){
                    $window.history.back();
                    return false;
                } else {
                    scope.close();
                }

            }

            if (scope.slyCallBack && typeof scope.slyCallBack == 'function'){
                scope.slyCallBack(evt);
            }

        });

        scope.$on('$destroy', function () {
            element.unbind('keydown');
        })
    }
}])
.directive('horizontalSly', ['$timeout', function ($timeout) {
    return function (scope, element, attrs) {

        scope.$on('slyLastElement', function () {

            var sly;

            // Call Sly on frame
            $timeout(function () {

                var $slidee = element.children().eq(0);
                var $wrap   = element.parent();

                sly = new Sly(element, {
                    horizontal: 1,
                    itemNav: 'forceCentered',
                    smart: 1,
                    activateOn: 'click',
                    mouseDragging: 1,
                    touchDragging: 1,
                    releaseSwing: 1,
                    startAt: 0,
                    scrollBar: $wrap.find('.scrollbar'),
                    scrollBy: 1,
                    activatePageOn: 'click',
                    speed: 300,
                    elasticBounds: 1,
                    easing: 'easeOutExpo',
                    dragHandle: 1,
                    dynamicHandle: 1,
                    clickBar: 1,

                    // Buttons
                    prev: $wrap.find('.prev'),
                    next: $wrap.find('.next')
                }).init();
            }, 0);

            scope.slyCallBack = function (evt) {

                if (evt.keyCode == 37) {
                    sly.prev();
                }

                if (evt.keyCode == 39) {
                    sly.next();
                }
            };

            scope.slyInitComplete = true;
            scope.removeFromSly = function (index) {
                sly.remove(index);
            };

        });


    };

}])
.directive('checkLast', [function () {

    return function (scope, element, attrs) {
        if (scope.$last) {
            scope.$emit('slyLastElement')
        }
    };
}])
.directive('swipeEffect', ['$swipe', function ($swipe) {
    return function (scope, element, attrs) {
        $swipe.bind(element, {
            'move' : function () {
                element.addClass('swiping');
            },
            'end' : function () {
                element.removeClass('swiping');
            }
        })
    };
}]);