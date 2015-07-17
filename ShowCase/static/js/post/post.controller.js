angular.module('PostApp')
.controller('postController', ['$scope', 'postModel', 'progress', 'alert', function ($scope, postModel, progress, alert) {
    $scope.init = function (userId, post_id) {
        if (angular.isUndefined($scope.post)){
            postModel.getPost(userId, post_id).then(function (post) {
                $scope.post = post;
            });
        }
    };

    $scope.vote = function (vote) {
        progress.showProgress();
        postModel.vote($scope.post.id, vote).then(function (response) {
            progress.hideProgress();
            $scope.post.vote.total = response.total;
            $scope.post.voting_status = vote ? "Positive" : "Negative";
        }, function () {
            progress.hideProgress();
            alert.showAlert("Can not process your response");
        });
    };

    $scope.toggleShowComments = function () {
        $scope.post.showComments = !$scope.post.showComments;
        if ($scope.post.showComments) {
            getComments();
        };
    };

    $scope.addComment = function (comment) {
        progress.showProgress();
        postModel.addComment($scope.post.id, comment).then(function (res) {
            progress.hideProgress();
            $scope.post.comments.push(res);
            $scope.post.comments_count += 1;
            $scope.post.comment = "";
        }, function () {
            progress.hideProgress();
            alert.showAlert("Unable to comment on this post");
        });
    };

    var getComments = function (index) {
        progress.showProgress();
        postModel.getComments($scope.post.id).then(function (res) {
            progress.hideProgress();
            $scope.post.comments = res;
        }, function () {
            progress.hideProgress();
            alert.showAlert("Could not get comment for this post");
        });
    };
}]).directive('elastic', [
    '$timeout',
    function($timeout) {
        return {
            restrict: 'A',
            link: function($scope, element) {
                $scope.initialHeight = $scope.initialHeight || element[0].offsetHeight;
                var resize = function() {
                    element[0].style.height = "" + $scope.initialHeight + "px";
                    if (element[0].value != ""){
                        element[0].style.height = "" + element[0].scrollHeight + "px";
                    }
                };
                element.on("blur input keyup change", resize);
                // $timeout(resize);
            }
        };
    }
]);