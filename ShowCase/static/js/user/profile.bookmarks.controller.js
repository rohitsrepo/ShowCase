angular.module('UserApp')
.controller('profileBookmarksController', ['$scope',
    '$state',
    'userModel',
    'bookmarkModel',
    'bookService',
    'progress',
    'alert',
    'usermodalService',
    'bucketmodalService',
    'shareModalService',
    function ($scope,
        $state,
        userModel,
        bookmarkModel,
        bookService,
        progress,
        alert,
        usermodalService,
        bucketmodalService,
        shareModalService) {
    $scope.bookmarks = [];
    $scope.math = window.Math;
    $scope.bookmarksMeta = {pageVal: 1, disableGetMore: false, busy: false, next:'', previous:'', noWorks: false};

    var getCompositions = function () {

        if (!$scope.bookmarksMeta.disableGetMore) {
            var pageVal = $scope.bookmarksMeta.pageVal;
            progress.showProgress();
            bookmarkModel.getBookMarks($scope.artist.id, pageVal).then(function (response) {
                $scope.bookmarksMeta.next = response.next;
                $scope.bookmarksMeta.previous = response.previous;

                for (var i = 0; i < response.results.length; i++) {
                    console.log(response.results[i]);
                    $scope.bookmarks.push(response.results[i]);
                }

                if (response.next == null){
                    $scope.bookmarksMeta.disableGetMore = true;
                }

                if ($scope.bookmarks.length == 0){
                    console.log('settion it to false');
                    $scope.bookmarksMeta.noWorks = true;
                }

                progress.hideProgress();
                $scope.bookmarksMeta.busy = false;
            }, function () {
                alert.showAlert('We are facing some problems fetching data');
                progress.hideProgress();
            });
        }

        $scope.bookmarksMeta.pageVal += 1;
    };

    $scope.loadMoreBookmarks = function () {
        if ($scope.bookmarksMeta.busy) {
            return;
        }

        $scope.bookmarksMeta.busy = true;
        getCompositions();
    }

    $scope.handleBookMark = function (index) {
        var art = $scope.bookmarks[index].content;
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

    $scope.showArtBuckets = function (index) {
        var art = $scope.bookmarks[index].content;
        bucketmodalService.showArtBuckets(art);
    }

    $scope.showAddToBucket = function (index) {
        var art = $scope.bookmarks[index].content;
        bucketmodalService.showAddToBucket(art);
    };

    $scope.toggleNsfw = function (index) {
        var art = $scope.bookmarks[index].content;
        art.nsfw = false;
    };

    $scope.shareArt = function (index) {
        var art = $scope.bookmarks[index].content;
        var base_url = "http://thirddime.com";
        var share_url = base_url + "/arts/" + art.slug;
        var title = 'Artwork: "' + art.title + '" by: ' + art.artist.name;
        var description = 'Find thoughts about artwork "' + art.title+
            '" at ' + share_url;
        var media = 'http://thirddime.com' + art.matter;
        shareModalService.shareThisPage(share_url, title, description, media);
    };

}]);