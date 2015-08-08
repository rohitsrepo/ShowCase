angular.module('UserApp')
.controller('profilePaintingsController', ['$scope',
    '$state',
    'userModel',
    'bookService',
    'progress',
    'alert',
    'usermodalService',
    function ($scope, $state, userModel, bookService, progress, alert, usermodalService) {
    $scope.arts = [];
    $scope.artsMeta = {pageVal: 1, disableGetMore: false, busy: false, next:'', previous:'', noWorks: false};

    var artFetcher = function () {
        var listType = $state.current.data.listType

        if (listType == 'paintings'){
            return userModel.getCompositions;
        } else if (listType == 'uploads') {
            return userModel.getUploads;
        } else if (listType == 'bookmarks') {
            return userModel.getBookMarks
        }
    }();

    var getCompositions = function () {

        if (!$scope.artsMeta.disableGetMore) {
            var pageVal = $scope.artsMeta.pageVal;
            progress.showProgress();
            artFetcher($scope.artist.id, pageVal).then(function (response) {
                $scope.artsMeta.next = response.next;
                $scope.artsMeta.previous = response.previous;

                for (var i = 0; i < response.results.length; i++) {
                    $scope.arts.push(response.results[i]);
                }

                if (response.next == null){
                    $scope.artsMeta.disableGetMore = true;
                }

                if ($scope.arts.length == 0){
                    console.log('settion it to false');
                    $scope.artsMeta.noWorks = true;
                }

                progress.hideProgress();
                $scope.artsMeta.busy = false;
            }, function () {
                alert.showAlert('We are facing some problems fetching data');
                progress.hideProgress();
            });
        }

        $scope.artsMeta.pageVal += 1;
    };

    $scope.loadMoreCompositions = function () {
        if ($scope.artsMeta.busy) {
            return;
        }

        $scope.artsMeta.busy = true;
        getCompositions();
    }

    $scope.handleBookMark = function (index) {
        art = $scope.arts[index]
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
        var art = $scope.arts[index];

        usermodalService.showBookMarkers(art).then(function (bookStatus) {
            if (bookStatus == 'bookmarked') {
                console.log("mark it booked");
                art.is_bookmarked = true;
            }
        });
    };

}]);