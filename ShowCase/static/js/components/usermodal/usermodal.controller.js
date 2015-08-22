angular.module('module.usermodal')
.controller('usermodalController', ['$scope',
    'compositionModel',
    'userModel',
    'close',
    'bookService',
    'followService',
    'target',
    'auth',
    'progress',
    'alert',
    'modalType',
    function ($scope, compositionModel, userModel, close, bookService, followService, target, auth, progress, alert, modalType) {

        var getNoUserInfo = function () {
            if (modalType == 'bookmarkers') {
                return 'No admirers yet';
            } else if (modalType == 'follows') {
                return 'User is not following anyone yet';
            } else if (modalType == 'followers') {
                return 'User is not followed by anyone yet';
            }
        };

        var getNoUserMessage = function () {
            if (modalType == 'bookmarkers') {
                return 'Do you find this work praise-worthy?';
            } else if (modalType == 'follows') {
                return '';
            } else if (modalType == 'followers') {
                return 'Is there a hint of matching taste?';
            }
        };

        var getNoUserActionMessage = function () {
            if (modalType == 'bookmarkers') {
                return 'ADMIRE';
            } else if (modalType == 'follows') {
                return '';
            } else if (modalType == 'followers') {
                return 'FOLLOW';
            }
        };

        var getActionResult = function () {
            if (modalType == 'bookmarkers') {
                return 'bookmarked';
            } else if (modalType == 'follows') {
                return '';
            } else if (modalType == 'followers') {
                return 'followed';
            }
        };

        var getNoUserAction = function () {
            if (modalType == 'bookmarkers') {
                return function () {
                    bookService.bookmark(target).then(function () {
                        close(getActionResult());
                    })
                };
            } else if (modalType == 'follows') {
                return function () {};
            } else if (modalType == 'followers') {
                return function () {
                    followService.follow(target).then(function () {
                        close(getActionResult());
                    })
                };
            }
        };

        $scope.noSuchUser = {
            status: false,
            info: getNoUserInfo(),
            message: getNoUserMessage(),
            actionMessage: getNoUserActionMessage(),
            action: getNoUserAction()
        };

        var userFetcher = function () {
            if (modalType == 'bookmarkers') {
                return compositionModel.getBookMarkers;
            } else if (modalType == 'follows') {
                return userModel.getFollows;
            } else if (modalType == 'followers') {
                return userModel.getFollowers;
            }
        }();

        progress.showProgress();
        userFetcher(target.id).then(function (bookmarkers) {
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