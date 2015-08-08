angular.module('module.bookmark')
.controller('bookmarkController', ['$scope', 'compositionModel', 'userModel', 'close', 'bookService', 'composition', 'auth', 'progress', 'alert',
    function ($scope, compositionModel, userModel, close, bookService, composition, auth, progress, alert) {

        $scope.noSuchUser = {
            status: false,
            info: 'No admirers yet',
            message: 'Do you find this praise-worthy?',
            actionMessage: 'ADMIRE',
            action: function () {
                console.log("calling the book bookService")
                bookService.bookmark(composition).then(function () {
                    close('bookmarked');
                })
            }
        };

        progress.showProgress();
        compositionModel.getBookMarkers(composition.id).then(function (bookmarkers) {
            $scope.bookmarkers = bookmarkers;

            if ($scope.bookmarkers.length == 0) {
                console.log('no such works found');
                $scope.noSuchUser.status = true;
            }

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
            var targetUser = $scope.bookmarkers[index];
            auth.runWithAuth(function () {
                if (targetUser.is_followed) {
                    unfollow(targetUser);
                } else {
                    follow(targetUser);
                }
            });
        };

    }
]);