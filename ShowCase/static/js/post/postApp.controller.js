angular.module('PostApp')
.controller('postAppController', ['$scope', 'postModel', 'progress', 'alert', function ($scope, postModel, progress, alert) {
    $scope.init = function (userId, post_id) {
        if (angular.isUndefined($scope.post)){
            progress.showProgress();
            postModel.getPost(userId, post_id).then(function (post) {
                $scope.post = post;
                progress.hideProgress();
            }, function () {
                progress.hideProgress();
                alert.showAlert("Unable to get related post");
            });
        }
    };
}]);