angular.module('PostApp')
.controller('postController', ['$scope', 'postModel', 'progress', 'alert', function ($scope, postModel, progress, alert) {
    $scope.vote = function (vote, post) {
        progress.showProgress();
        postModel.vote(post.id, vote).then(function (response) {
            progress.hideProgress();
            post.vote.total = response.total;
            post.voting_status = vote ? "Positive" : "Negative";
        }, function () {
            progress.hideProgress();
            alert.showAlert("Can not process your response");
        });
    };

    $scope.toggleShowComments = function (post) {
        post.showComments = !post.showComments;
        if (post.showComments) {
            getComments(post);
        };
    };

    $scope.addComment = function (comment, post) {
        progress.showProgress();
        postModel.addComment(post.id, comment).then(function (res) {
            progress.hideProgress();
            post.comments.push(res);
            post.comments_count += 1;
            post.comment = "";
        }, function () {
            progress.hideProgress();
            alert.showAlert("Unable to comment on this post");
        });
    };

    var getComments = function (post) {
        progress.showProgress();
        postModel.getComments(post.id).then(function (res) {
            progress.hideProgress();
            post.comments = res;
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

                $scope.$watch(function () {
                    return element[0].value;
                }, function (val) {
                    if (val == ""){
                        element[0].style.height = "" + $scope.initialHeight + "px";
                    } else {
                        element[0].style.height = "" + element[0].scrollHeight + "px";
                    }
                });
            }
        };
    }
]);