angular.module('module.follow', ['module.model', 'module.util'])
.factory('followService', ['$q', 'userModel', 'progress', 'alert', function ($q, userModel, progress, alert) {
    var service = {};

    service.follow = function (targetUser) {
        progress.showProgress();

        return userModel.follow(targetUser.id).then(function (response) {
            progress.hideProgress();
            return $q.when();
        }, function () {
            progress.hideProgress();
            alert.showAlert('We are unable to process your response');
            return $q.reject();
        });
    };

    service.unfollow = function (targetUser) {
        progress.showProgress();

        return userModel.unfollow(targetUser.id).then(function (response) {
            progress.hideProgress();
            return $q.when();
        }, function () {
            progress.hideProgress();
            alert.showAlert('We are unable to process your response');
            return $q.reject();
        });
    };

    return service;
}]);