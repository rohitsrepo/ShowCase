angular.module('module.usermodal')
.controller('usermodalController', ['$scope',
    'compositionModel',
    'userModel',
    'close',
    'bookService',
    'followService',
    'inputData',
    'auth',
    'progress',
    'alert',
    function ($scope, compositionModel, userModel, close, bookService, followService, inputData, auth, progress, alert) {

        $scope.noSuchUser = {
            status: false,
            info: inputData.noUserInfo,
            message: inputData.noUserMessage,
            actionMessage: inputData.noUserActionMessage,
            action: function () {
                inputData.noUserAction().then(function () {
                    close(inputData.noUserActionResult);
                })
            }
        };

        $scope.holdClick = function(event) {
            event.stopPropagation();
        };

        progress.showProgress();
        inputData.usersFetcher().then(function (bookmarkers) {
            $scope.bookmarkers = bookmarkers;

            if ($scope.bookmarkers.length == 0) {
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

        $scope.handleFollow = function (index) {
            var targetUser = $scope.bookmarkers[index];
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

    }
]);