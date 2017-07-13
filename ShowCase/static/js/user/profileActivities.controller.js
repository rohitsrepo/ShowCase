angular.module('UserApp')
.controller('profileActivitiesController', ['$scope',
    'activityModel',
    'bucketmodalService',
    'bookService',
    'admireService',
    'usermodalService',
    'shareModalService',
    'progress',
    'alert',
    function ($scope,
        activityModel,
        bucketmodalService,
        bookService,
        admireService,
        usermodalService,
        shareModalService,
        progress,
        alert) {

        $scope.math = window.Math;
        $scope.userActivities = [];
        $scope.activitiesMeta = {next_token: '', disableGetMore: false, busy: false, noActivities: false};

        var mq = window.matchMedia( "(max-width: 800px)" );
        if (mq.matches) {
            $scope.onMobile = true;
        }
        else {
            $scope.onMobile = false;
        }

        var classifyActivity = function (activity) {
            switch (activity.post_type){
                case 'CR':
                case 'MA':
                case 'AD':
                    return 1;
                case 'BK':
                    return 2;
                case 'MB':
                    return 3;
                case 'IN':
                case 'AI':
                    return 4;
                default:
                    console.log('Invalid activity type found', activity.post_type);
            };
        };

        var getActivities = function () {

            if (!$scope.activitiesMeta.disableGetMore) {
                var next_token = $scope.activitiesMeta.next_token;
                progress.showProgress();
                activityModel.userActivities($scope.artist.id, next_token).then(function (response) {
                    $scope.activitiesMeta.next_token = response.next_token;

                    var activity;
                    for (var i = 0; i < response.results.length; i++) {
                        activity = response.results[i];
                        activity['grade'] = classifyActivity(activity);

                        $scope.userActivities.push(activity);
                    }

                    if (response.next_token == ""){
                        $scope.activitiesMeta.disableGetMore = true;
                    }

                    if ($scope.userActivities.length == 0){
                        $scope.activitiesMeta.noActivities = true;
                    }

                    progress.hideProgress();
                    $scope.activitiesMeta.busy = false;
                }, function () {
                    alert.showAlert('We are unable to fetch data');
                    progress.hideProgress();
                });
            }
        };

        $scope.loadMoreActivities = function () {
            if ($scope.activitiesMeta.busy) {
                return;
            }

            $scope.activitiesMeta.busy = true;
            getActivities();
        };

        $scope.showBucketArts = function (index) {
            var activity = $scope.userActivities[index];
            bucketmodalService.showBucketArts(activity.content);
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

        $scope.shareBucket = function (event, bucket) {
            // Stop route change on click
            event.stopPropagation();

            var base_url = "http://thirddime.com";
            var share_url = base_url + "/@" + bucket.owner.slug + '/series/' + bucket.slug;
            var title = 'Series: "' + bucket.name + '" by: ' + bucket.owner.name;
            var description = bucket.description + '...Complete series can be found at: ' + share_url;
            var media = 'http://thirddime.com' + bucket.picture;
            shareModalService.shareThisPage(share_url, title, description, media);
        };

        $scope.handleBookMarkBucket = function (event, bucket) {
            event.stopPropagation();

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

        $scope.handleAdmireBucket = function (event, bucket) {
            event.stopPropagation();

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

        $scope.handleBookmarkInterpret = function (interpret) {
            if (interpret.is_bookmarked) {
                bookService.unmarkInterpret(interpret).then(function () {
                    interpret.is_bookmarked = false;
                });
            } else {
                bookService.bookmarkInterpret(interpret).then(function () {
                    interpret.is_bookmarked = true;
                });;
            }
        };

        $scope.getTextColor = function (color) {
            var red = parseInt(color.substring(1,3), 16);
            var green = parseInt(color.substring(3,5), 16);
            var blue = parseInt(color.substring(5), 16);

            var lum = 1 - ( 0.299 * red + 0.587 * green + 0.114 * blue)/255;

            if (lum > 0.5){
                return 'white';
            }

            return 'black';
        }

        $scope.showArtBuckets = function (art) {
            bucketmodalService.showArtBuckets(art);
        }

        $scope.showAddToBucket = function (event, art) {
            event.stopPropagation();
            bucketmodalService.showAddToBucket(art);
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
    }
]);