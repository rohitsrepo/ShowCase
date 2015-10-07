angular.module('BucketApp')
.controller('bucketController', ['$scope',
    '$rootScope',
    '$document',
    'auth',
    'bucketModel',
    'bookService',
    'followBucketService',
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
        followBucketService,
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

        var getArts = function (bucketId) {

            bucketModel.bucketArts(bucketId).then(function (arts) {
                if (arts.length > 0){
                    $scope.bucketArts = arts;
                    $scope.bucketArts[currentShowIndex].show = true;
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
        $scope.init = function (id, name, description, background, slug, owner, is_watched, is_bookmarked, isMe) {
            $scope.bucket.id = id;
            $scope.bucket.slug = slug;
            $scope.bucket.name = name;
            $scope.bucket.description = description;
            $scope.bucket.background = background;
            $scope.bucket.owner = owner;
            $scope.bucket.isWatched = is_watched == 'True';
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

        $scope.watchBucket = function () {
            followBucketService.watchBucket($scope.bucket.id).then(function () {
                $scope.bucket.isWatched = true;
            });
        };

        $scope.unwatchBucket = function () {
            followBucketService.unwatchBucket($scope.bucket.id).then(function () {
                $scope.bucket.isWatched = false;
            });
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
            var title = 'Series: "' + $scope.bucket.name + '" by: ' + $scope.bucket.owner
            var description = $scope.bucket.description + '...Complete series can be found at: ' + share_url;
            var media = 'http://thirddime.com' + $scope.bucket.background;
            shareModalService.shareThisPage(share_url, title, description, media);
        };

        $scope.editBucketMembership = function (index) {
            var membership = $scope.bucketArts[index];
            bucketmodalService.showEditBucketMembership($scope.bucket, membership);
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