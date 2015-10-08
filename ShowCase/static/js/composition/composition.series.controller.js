angular.module('CompositionSeriesApp')
.controller('compositionSeriesController', ['$scope',
    '$rootScope',
    '$document',
    'bucketModel',
    'bucketmodalService',
    'bookService',
    'admireService',
    'progress',
    'alert',
    function ($scope,
        $rootScope,
        $document,
        bucketModel,
        bucketmodalService,
        bookService,
        admireService,
        progress,
        alert) {

        // Disable scroll on parent page
        $rootScope.$on('$stateChangeSuccess',
        function(event, toState, toParams, fromState, fromParams){
            var body = $document.find('body');
            body.addClass('modal-open');

            if (toState.name == 'buckets') {
                body.removeClass('modal-open');
            }
        });

        $scope.noSuchBucket = {
            status: false,
            action: function () {
                bucketmodalService.showAddToBucket(art);
                close();
            }
        };

        var getSeries = function (artId) {
            progress.showProgress();

            bucketModel.artBuckets(artId).then(function (buckets) {
                $scope.artBuckets = buckets;

                if ($scope.artBuckets.length == 0){
                    $scope.noSuchBucket.status = true;
                }

                progress.hideProgress();
            }, function () {
                alert.showAlert('We are unable to fetch data');
                progress.hideProgress();
            });
        };

        $scope.art = [];
        $scope.init = function (id, url, slug, title, isBookMarked) {
            $scope.art.id = id;
            $scope.art.url = url;
            $scope.art.slug = slug;
            $scope.art.title = title;
            $scope.art.is_bookMarked = isBookMarked == 'True';

            getSeries(id);
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


    }
]);