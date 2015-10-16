angular.module('module.bucketmodal')
.controller('bucketmodalContentController', ['$scope',
    '$window',
    '$state',
    'auth',
    'bucketModel',
    'bookService',
    'admireService',
    'followService',
    'bucketmodalService',
    'confirmModalService',
    'shareModalService',
    'close',
    'bucket',
    'progress',
    'alert',
    function ($scope,
        $window,
        $state,
        auth,
        bucketModel,
        bookService,
        admireService,
        followService,
        bucketmodalService,
        confirmModalService,
        shareModalService,
        close,
        bucket,
        progress,
        alert) {

        progress.showProgress();
        $scope.bucket = bucket;
        $scope.noArts = false;
        $scope.math = window.Math;
        $scope.isState = $state.current.data && $state.current.data.isState;
        var currentShowIndex = 0;

        var admirationOptions = angular.copy(admireService.admirationOptions);
        admirationOptions.splice(0,1);
        $scope.admirationOptions = [];
        var currentOptionIndex = -1;

        for(i=0; i< admirationOptions.length; i++){
            $scope.admirationOptions.push({
                'word': admirationOptions[i],
                'count': 0,
                'id': 0
            });
        }


        var getAdmirationOptions = function () {
            admireService.getAdmirationOptionsBucket($scope.bucket).then(function (options) {

                for(i=0; i< $scope.admirationOptions.length; i++){
                    for(j=0; j< options.length; j++){
                        if ($scope.admirationOptions[i].word === options[j].word){
                            $scope.admirationOptions[i].count = options[j].count;
                            $scope.admirationOptions[i].id = options[j].id;

                            if (options[j].id == $scope.bucket.admire_as){
                                currentOptionIndex = i;
                                $scope.admirationOptions[i].selected = true;
                            }

                            break;
                        }
                    }
                }
            });
        };

        bucketModel.bucketArts(bucket.id).then(function (arts) {
            if (arts.length > 0){
                $scope.bucketArts = arts;
                $scope.bucketArts[currentShowIndex].show = true;
                getAdmirationOptions();
            } else {
                $scope.noArts = true;
            }

            progress.hideProgress();
        }, function () {
            alert.showAlert('We are currently unable to get art for this series');
            progress.hideProgress();
        });

        $scope.makeBucketPublic = function () {
            bucketModel.makeBucketPublic($scope.bucket.id).then(function () {
                $scope.bucket.is_public = true;
            });
        };


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

        $scope.handleBookMarkBucket = function () {
            var bucket = $scope.bucket;
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

        $scope.removeFromBucket = function (index) {
            progress.hideProgress();
            var membership = $scope.bucketArts[index];

            confirmModalService.showDeleteConfirm().then(function () {
                bucketModel.removeFromBucket($scope.bucket.id, membership.composition.id).then(function () {
                    $scope.removeFromSly(index);
                    if (membership.description) {
                        $scope.removeFromSly(index - 1);
                    }

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

        $scope.editBucketMembership = function (index) {
            var membership = $scope.bucketArts[index];
            bucketmodalService.showEditBucketMembership($scope.bucket, membership);
        };

        $scope.admireBucket = function (index){
            if (index == currentOptionIndex) {
                return;
            }

            var option = $scope.admirationOptions[index];
            var bucket = $scope.bucket;
            admireService.admireBucket(bucket, option.word).then(function () {
                if (bucket.is_admired && currentOptionIndex >=0 ) {
                    $scope.admirationOptions[currentOptionIndex].selected=false;
                    $scope.admirationOptions[currentOptionIndex].count--;
                }

                bucket.is_admired = true;
                option.count++;
                option.selected = true;
                currentOptionIndex = index;
            });
        }

        $scope.handleAdmireBucket = function () {
            var bucket = $scope.bucket;

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

        $scope.shareArt = function (index) {
            var art = $scope.bucketArts[index].composition;
            var base_url = "http://thirddime.com";
            var share_url = base_url + "/arts/" + art.slug;
            var title = 'Artwork: "' + art.title + '" by: ' + art.artist.name;
            var description = 'Find thoughts about artwork "' + art.title+
                '" at ' + share_url;
            var media = 'http://thirddime.com' + art.matter;
            shareModalService.shareThisPage(share_url, title, description, media);
        };

        $scope.showAddToBucket = function (index) {
            var art = $scope.bucketArts[index].composition;
            bucketmodalService.showAddToBucket(art);
        };

        $scope.handleBookMarkArt = function (index) {
            var art = $scope.bucketArts[index].composition;

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
            var art = $scope.bucketArts[index].composition;

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

        $scope.handleFollow = function () {
            var targetUser = $scope.bucket.owner;
            if (targetUser.is_followed) {
                followService.unfollow(targetUser).then(function () {
                    targetUser.is_followed = false;
                });
            } else {
                followService.follow(targetUser).then(function () {
                    targetUser.is_followed = true;
                });
            }
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
                    // scope.close();
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