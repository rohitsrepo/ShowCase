var notificationModule = angular.module('notification.module', ['artifact.notification']);

notificationModule.controller('notificationController', ['$scope', 'getUser', 'notificationFactory', function ($scope, getUser, notificationFactory) {
    'use strict';
    $scope.notifications = [];
    
    notificationFactory.getNotifications().then(function (res) {
        $scope.notifications = res;
        angular.forEach($scope.notifications, function (value, key) {
            if (value.unread) {
                notificationFactory.markAsRead(value.id);
            }
        });
    }, function (res) {});
}]);