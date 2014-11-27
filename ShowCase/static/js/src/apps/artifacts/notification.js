var notificationModule = angular.module('artifact.notification', []);

notificationModule.factory('notificationFactory', ['$http', '$log', '$interval', function ($http, $log, $interval) {
    'use strict';
    
    var service = {};
    service.newNotification = false;
    
    var checkForNotification = function () {
        return $http({method: 'GET', url: 'notifications/check'}).then(function (res) {
            $log.info(res.data.result);
            service.newNotification = res.data.result;
        }, function (res) {
            $log.error('Checking for new notifications ', res);
        });
    };
    
    $interval(checkForNotification, 50000);
    
    service.getNotifications = function () {
        return $http({method: 'GET', url: '/notifications'}).then(function (res) {
            return res.data;
        }, function (res) {
            $log.error('Getting notifications for the user', res);
        });
    };
    
    service.markAsRead = function (notificationId) {
        return $http({method: 'GET', url: 'notifications/mark-as-read/' + notificationId}).then(function (res) {}, function (res) {
            $log.error("Marking notification read.", res);
        });
    };
    
    service.markAllRead = function () {
        return $http({method: 'GET', url: 'notifications/mark-all-as-read'}).then(function (res) {}, function (res) {
            $log.error("Marking all notifications read.", res);
        });
    };
    
    return service;
}]);