angular.module('module.shareModal')
.controller('shareModalController', ['$scope',
    'actions',
    'close',
    'progress',
    'alert',
    function ($scope, actions, close, progress, alert) {
        $scope.actions = actions;

        $scope.close = function () {
            close();
        };

    }
]);