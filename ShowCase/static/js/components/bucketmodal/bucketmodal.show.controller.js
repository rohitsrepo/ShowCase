angular.module('module.bucketmodal')
.controller('bucketmodalShowController', ['$scope',
    'bucketModel',
    'bucketmodalService',
    'followBucketService',
    'shareModalService',
    'bookService',
    'admireService',
    'close',
    'art',
    'progress',
    'alert',
    function ($scope,
        bucketModel,
        bucketmodalService,
        followBucketService,
        shareModalService,
        bookService,
        admireService,
        close,
        art,
        progress,
        alert) {

        $scope.noSuchBucket = {
            status: false,
            action: function () {
                bucketmodalService.showAddToBucket(art);
                close();
            }
        }

        $scope.bucketForShowLoaded = false;
        $scope.art = art;
        bucketModel.artBuckets(art.id).then(function (buckets) {
            $scope.showArtBuckets = buckets;
            $scope.bucketForShowLoaded = true;

            if ($scope.showArtBuckets.length == 0){
                $scope.noSuchBucket.status = true;
            }

        }, function () {
            alert.showAlert('We are unable to fetch data');
            $scope.bucketForShowLoaded = true;
        });

        $scope.showArts = function (index) {
            var bucket = $scope.showArtBuckets[index];
            bucketmodalService.showBucketArts(bucket);
        }

        $scope.close = function () {
            close();
        };

        $scope.shareBucket = function (event, index) {
            // Stop route change on click
            event.stopPropagation();

            var bucket = $scope.showArtBuckets[index];
            var base_url = "http://thirddime.com";
            var share_url = base_url + "/@" + bucket.owner.slug + '/series/' + bucket.slug;
            var title = 'Series: "' + bucket.name + '" by: ' + bucket.owner.name;
            var description = bucket.description + '...Complete series can be found at: ' + share_url;
            var media = 'http://thirddime.com' + bucket.picture;
            shareModalService.shareThisPage(share_url, title, description, media);
        };

        $scope.watchBucket = function (event, index) {
            // Stop route change on click
            event.stopPropagation();

            var bucket = $scope.showArtBuckets[index];
            followBucketService.watchBucket(bucket.id).then(function () {
                bucket.is_watched = true;
            });
        };

        $scope.unwatchBucket = function (event, index) {
            // Stop route change on click
            event.stopPropagation();

            var bucket = $scope.showArtBuckets[index];
            followBucketService.unwatchBucket(bucket.id).then(function () {
                bucket.is_watched = false;
            });
        };

        $scope.handleBookMarkBucket = function (event, index) {
            event.stopPropagation();

            var bucket = $scope.showArtBuckets[index];
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

            var bucket = $scope.showArtBuckets[index];
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
    }
])
.directive('keyEventBinderShow', ['$window', function ($window) {
    return function (scope, element, attrs) {
        element.focus();
        element.bind('keydown', function (evt) {

            if (evt.keyCode == 27) {
                $window.history.back();
                return false;
            }
        });

        scope.$on('$destroy', function () {
            element.unbind('keydown');
        })
    }
}]);