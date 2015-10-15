angular.module('BucketApp')
.controller('bucketController', ['$scope',
    '$rootScope',
    '$document',
    'auth',
    'bucketModel',
    'bookService',
    'admireService',
    'followService',
    'bucketmodalService',
    'confirmModalService',
    'shareModalService',
    'progress',
    'alert',
    function ($scope,
        $rootScope,
        $document,
        auth,
        bucketModel,
        bookService,
        admireService,
        followService,
        bucketmodalService,
        confirmModalService,
        shareModalService,
        progress,
        alert) {

        $scope.noSuchBucket = {
            status: false,
            action: function () {
                bucketmodalService.showAddToBucket(art);
                close();
            }
        };

        $scope.math = window.Math;
        $scope.noArts = false;
        var currentShowIndex = 0;

        var admirationOptions = angular.copy(admireService.admirationOptions);
        admirationOptions.splice(0,1);
        $scope.admirationOptions = [];
        var currentOptionIndex = -1;

        for(i=0; i< admirationOptions.length; i++){
            $scope.admirationOptions.push({
                'word': admirationOptions[i],
                'count': -1,
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

                        if ($scope.admirationOptions[i].count == -1) {
                            $scope.admirationOptions[i].count = 0;
                        }
                    }
                }
            });
        };

        var getArts = function (bucketId) {

            bucketModel.bucketArts(bucketId).then(function (arts) {
                if (arts.length > 0){
                    $scope.bucketArts = arts;
                    $scope.bucketArts[currentShowIndex].show = true;
                    getAdmirationOptions();
                } else {
                    $scope.noArts = true;
                }
                progress.hideProgress();
            }, function () {
                alert.showAlert('We are unable to art for this series');
                progress.hideProgress();
            });
        };

        $scope.bucket = {};
        $scope.init = function (id, name, description, background, slug, ownerName, ownerId, ownerSlug, ownerIsFollowed, is_admired, admire_as, is_bookmarked, isMe) {
            $scope.bucket.id = id;
            $scope.bucket.slug = slug;
            $scope.bucket.name = name;
            $scope.bucket.description = description;
            $scope.bucket.background = background;
            $scope.bucket.owner = {'name': ownerName,
                                    'id': ownerId,
                                    'slug': ownerSlug,
                                    'is_followed': ownerIsFollowed == 'True'};
            $scope.bucket.is_admired = is_admired == 'True';
            $scope.bucket.admire_as = admire_as;
            $scope.bucket.is_bookmarked = is_bookmarked == 'True';

            $scope.isMe = isMe == 'True';

            getArts(id);

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
                    window.location.href = '/arts';
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
            var share_url = window.location.href;
            var title = 'Series: "' + $scope.bucket.name + '" by: ' + $scope.bucket.owner['name'];
            var description = $scope.bucket.description + '...Complete series can be found at: ' + share_url;
            var media = 'http://thirddime.com' + $scope.bucket.background;
            shareModalService.shareThisPage(share_url, title, description, media);
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
                if (bucket.is_admired) {
                    $scope.admirationOptions[currentOptionIndex].selected=false;
                    $scope.admirationOptions[currentOptionIndex].count--;
                }

                bucket.is_admired = true;
                option.count++;
                option.selected = true;
                currentOptionIndex = index;
            });
        }

        $scope.handleAdmireBucket = function (option) {
            var bucket = $scope.bucket;

            if (bucket.is_admired) {
                admireService.unadmireBucket(bucket).then(function () {
                    bucket.is_admired = false;
                });
            } else {
                admireService.admireBucket(bucket, option).then(function () {
                    bucket.is_admired = true;
                });;
            }
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
.directive('keyEventBinderContentSolo', ['$window', function ($window) {
    return function (scope, element, attrs) {
        element.focus();
        element.bind('keydown', function (evt) {
            scope.slyCallBack(evt);
        });

        scope.$on('$destroy', function () {
            element.unbind('keydown');
        })
    }
}]);