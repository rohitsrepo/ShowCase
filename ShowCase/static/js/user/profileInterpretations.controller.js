angular.module('UserApp')
.controller('profilePostsController', ['$scope', 'postModel', 'progress', 'alert', function ($scope, postModel, progress, alert) {
    $scope.postsMeta = {pageVal: 1, disableGetMore: false, busy: false, next:'', previous:''};
    $scope.posts = [];

    var getPosts = function () {
        if (!$scope.postsMeta.disableGetMore) {
            var pageVal = $scope.postsMeta.pageVal;
            postModel.getUserPosts($scope.artist.id, pageVal).then(function (posts) {
                $scope.postsMeta.next = posts.next;
                $scope.postsMeta.previous = posts.previous;

                for (var i = 0; i < posts.results.length; i++) {
                    $scope.posts.push(posts.results[i]);
                }

                if (posts.next == null){
                    $scope.postsMeta.disableGetMore = true;
                    // analytics.logEvent('Reader', 'Load More posts - Hit Bottom');
                }

                progress.hideProgress();
                $scope.postsMeta.busy = false;
            }, function () {
                alert.showAlert('We are facing some problems fetching data');
                progress.hideProgress();
            });
        }

        $scope.postsMeta.pageVal += 1;
    }

    $scope.loadMorePosts = function () {
        if ($scope.postsMeta.busy) {
            return;
        }

        $scope.postsMeta.busy = true;
        if ($scope.posts.length != 0){
            // analytics.logEvent('Reader', 'Load More posts');
        } else {
            // analytics.logEvent('Reader', 'Init');
        }
        getPosts();
    };



}]);