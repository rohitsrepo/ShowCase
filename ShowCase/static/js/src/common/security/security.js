var securityModule = angular.module('security.service', ['artifact.user', 'helper.logger']);

securityModule.factory('securityFactory', function ($http, userFactory, logger) {
    'use strict';
    
    var service = {};

    service.currentUser = null;
    service.getCurrentUser = function () {
        if (!service.currentUser) {
            service.currentUser = userFactory.getCurrentUser.then(function (user) {
                return user;
            }, function (res) {
                // TODO remove this logging.
                logger('Security factory', res);
                return res;
            });
        }
        return service.currentUser;
    };
    
    return service;
});