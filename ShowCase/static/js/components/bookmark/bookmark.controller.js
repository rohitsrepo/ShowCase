angular.module('module.bookmark')
.controller('bookmarkController', ['$scope', 'compositionModel', 'userModel', 'close', 'composition', 'progress', 'alert',
    function ($scope, compositionModel, userModel, close, composition, progress, alert) {

        progress.showProgress();
        compositionModel.getBookMarkers(composition.id).then(function (bookmarkers) {
            $scope.bookmarkers = bookmarkers;
            progress.hideProgress();
        }, function () {
            alert.showAlert('We are unable to fetch data');
            progress.hideProgress();
        });

        $scope.close = function () {
            close();
        };

        var follow = function (targetUser) {
            progress.showProgress();

            userModel.follow(targetUser.id).then(function (response) {
                targetUser.is_followed = true;
                progress.hideProgress();
                console.log('Follow');
            }, function () {
                progress.hideProgress();
                alert.showAlert('We are unable to process your response');
            });
        };

        var unfollow = function (targetUser) {
            progress.showProgress();

            userModel.unfollow(targetUser.id).then(function (response) {
                targetUser.is_followed = false;
                progress.hideProgress();
                console.log('Unfollow');
            }, function () {
                progress.hideProgress();
                alert.showAlert('We are unable to process your response');
            });
        };

        $scope.handleFollow = function (index) {
            var targetUser = $scope.bookmarkers[index]
            if (targetUser.is_followed) {
                unfollow(targetUser);
            } else {
                follow(targetUser);
            }
        };

    }
]);