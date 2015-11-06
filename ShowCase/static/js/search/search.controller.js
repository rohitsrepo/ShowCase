angular.module('SearchApp')
.controller('searchController', ['$scope',
    '$state',
    '$q',
    '$location',
    'admireService',
    'bookService',
    'bucketmodalService',
    'shareModalService',
    'followService',
    'searchModel',
    'alert',
    'progress',
    function ($scope, $state, $q, $location, admireService, bookService, bucketmodalService, shareModalService, followService, searchModel, alert, progress) {
    $scope.searchmeta = {};
    $scope.math = window.Math;
    $scope.searchMeta = {
        pageVal: 1,
        disableGetMore: false,
        busy: false,
        next:'',
        previous:'',
        noWorks: false,
        results: []
    };

    var query = $location.search().q;
    if (query) {
        $scope.searchmeta.query = query;    
    }
    

    var mq = window.matchMedia( "(max-width: 800px)" );
    if (mq.matches) {
        $scope.onMobile = true;
    }
    else {
        $scope.onMobile = false;
    }

    // Disable scroll on parent page
    $scope.$on('$stateChangeSuccess',
    function(event, toState, toParams, fromState, fromParams){
        $scope.searchMeta = {
            pageVal: 1,
            disableGetMore: false,
            busy: false,
            next:'',
            previous:'',
            noWorks: false,
            results: []
        };
    });

    var artifactFetcher = function () {
        var current = $state.current.name;


        if (current == 'all') {
            return searchModel.search;
        } else if (current == 'users') {
            return searchModel.searchUsers;
        } else if (current == 'arts') {
            return searchModel.searchArts;
        } else if (current == 'buckets') {
            return searchModel.searchBuckets;
        } else {
            return function () {
                return $q.reject();
            };
        }

    };

    var getArtifacts = function () {

        if (!$scope.searchMeta.disableGetMore) {
            var pageVal = $scope.searchMeta.pageVal;
            progress.showProgress();

            artifactFetcher()($scope.searchmeta.query, pageVal).then(function (response) {
                $scope.searchMeta.next = response.next;
                $scope.searchMeta.previous = response.previous;

                for (var i = 0; i < response.results.length; i++) {
                    $scope.searchMeta.results.push(response.results[i]);
                }

                if (!response.next){
                    $scope.searchMeta.disableGetMore = true;
                }

                if (!$scope.searchMeta.results || $scope.searchMeta.results.length == 0){
                    $scope.searchMeta.noWorks = true;
                } else {
                    $scope.searchMeta.noWorks = false;
                }

                progress.hideProgress();
                $scope.searchMeta.busy = false;
            }, function () {
                progress.hideProgress();
            });
        }

        $scope.searchMeta.pageVal += 1;
    };

    $scope.loadMoreArtifacts = function () {
        if ($scope.searchMeta.busy || !$scope.searchmeta.query) {
            return;
        }

        $scope.searchMeta.busy = true;
        getArtifacts();
    }

    $scope.$watch(function () {
        return $scope.searchmeta.query;
    }, function (val) {
        if (val) {
            $scope.searchMeta = {
                pageVal: 1,
                disableGetMore: false,
                busy: false,
                next:'',
                previous:'',
                noWorks: false,
                results: []
            };

            getArtifacts();
        }
    });

    $scope.handleBookMark = function (event, index) {
        event.stopPropagation();
        var art = $scope.searchMeta.results[index].content_object;
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

    $scope.handleBookMarkBucket = function (event, index) {
        event.stopPropagation();

        var bucket = $scope.searchMeta.results[index].content_object;
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

    $scope.handleAdmireArt = function (event, index) {
        event.stopPropagation();
        var art = $scope.searchMeta.results[index].content_object;

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

    $scope.handleAdmireBucket = function (event, index) {
        event.stopPropagation();

        var bucket = $scope.searchMeta.results[index].content_object;
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

    $scope.showArtBuckets = function (index) {
        var art = $scope.searchMeta.results[index].content_object;
        bucketmodalService.showArtBuckets(art);
    }

    $scope.showAddToBucket = function (event, index) {
        event.stopPropagation();
        var art = $scope.searchMeta.results[index].content_object;
        bucketmodalService.showAddToBucket(art);
    };

    $scope.toggleNsfw = function (index) {
        var art = $scope.searchMeta.results[index].content_object;
        art.nsfw = false;
    };

    $scope.shareArt = function (event, index) {
        event.stopPropagation();
        var art = $scope.searchMeta.results[index].content_object;
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

        var bucket = $scope.searchMeta.results[index].content_object;
        var base_url = "http://thirddime.com";
        var share_url = base_url + "/@" + bucket.owner.slug + '/series/' + bucket.slug;
        var title = 'Series: "' + bucket.name + '" by: ' + bucket.owner.name;
        var description = bucket.description + '...Complete series can be found at: ' + share_url;
        var media = 'http://thirddime.com' + bucket.picture;
        shareModalService.shareThisPage(share_url, title, description, media);
    };

    $scope.handleFollow = function (targetUser) {

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

}])
.controller('searchAllController', ['$scope',
    'searchModel',
    'alert',
    'progress',
    function ($scope, searchModel, alert, progress) {


}]);