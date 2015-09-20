angular.module('MypostsApp')
.controller('mypostsController', ['$scope',
    '$rootScope',
    '$document',
    'auth',
    'activityModel',
    'bucketmodalService',
    'bookService',
    'usermodalService',
    'shareModalService',
    'progress',
    'alert',
    function ($scope,
        $rootScope,
        $document,
        auth,
        activityModel,
        bucketmodalService,
        bookService,
        usermodalService,
        shareModalService,
        progress,
        alert) {

    $scope.userActivities = [];
    $scope.activitiesMeta = {next_token: '', disableGetMore: false, busy: false, noPosts: false};

    // Disable scroll on parent page
    $rootScope.$on('$stateChangeSuccess',
    function(event, toState, toParams, fromState, fromParams){
        var body = $document.find('body');
        body.addClass('modal-open');

        if (toState.name == 'posts') {
            body.removeClass('modal-open');
        }
    });

    var getActivities = function () {

        if (!$scope.activitiesMeta.disableGetMore) {
            var next_token = $scope.activitiesMeta.next_token;
            progress.showProgress();
            activityModel.newsActivities($scope.user.id, next_token).then(function (response) {
                $scope.activitiesMeta.next_token = response.next_token;

                for (var i = 0; i < response.results.length; i++) {
                    $scope.userActivities.push(response.results[i]);
                }

                if (response.next_token == ""){
                    $scope.activitiesMeta.disableGetMore = true;
                }

                if ($scope.userActivities.length == 0){
                    $scope.activitiesMeta.noPosts = true;
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

        auth.getCurrentUser().then(function (user) {
            $scope.user = user;
            getActivities();
        });
    };

    $scope.showBucketArts = function (index) {
        var activity = $scope.userActivities[index];
        bucketmodalService.showBucketArts(activity.content);
    };

    $scope.handleBookMark = function (index) {
        art = $scope.userActivities[index].composition;
        if (art.is_bookmarked) {
            bookService.unmark(art).then(function () {
                art.is_bookmarked = false;
            });
        } else {
            bookService.bookmark(art).then(function () {
                art.is_bookmarked = true;
            });;
        }
    };

    $scope.showBookMarkers = function (index) {
        var art = $scope.userActivities[index].composition;

        usermodalService.showBookMarkers(art).then(function (bookStatus) {
            if (bookStatus == 'bookmarked') {
                art.is_bookmarked = true;
            }
        });
    };

    $scope.showArtBuckets = function (index) {
        var art = $scope.userActivities[index].composition;
        bucketmodalService.showArtBuckets(art);
    }

    $scope.showAddToBucket = function (index) {
        var art = $scope.userActivities[index].composition;
        bucketmodalService.showAddToBucket(art);
    };

    $scope.shareArt = function (index) {
        var art = $scope.userActivities[index].composition;
        var base_url = "http://thirddime.com";
        var share_url = base_url + "/arts/" + art.slug;
        var title = 'Artwork: "' + art.title + '" by: ' + art.artist.name;
        var description = 'Find thoughts about artwork "' + art.title+
            '" at ' + share_url;
        var media = 'http://thirddime.com' + art.matter;
        shareModalService.shareThisPage(share_url, title, description, media);
    };

}]);