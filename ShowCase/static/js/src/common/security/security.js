var securityModule = angular.module('security.service', ['artifact.user', 'helper.logger']);

securityModule.factory('securityFactory', function ($http, $q, userFactory, logger) {
    'use strict';
    
    var service = {};
    service.currentUser = null;
    
    service.getCurrentUser = function () {
        if (!service.currentUser) {
            return userFactory.getCurrentUser().then(function (user) {
                service.currentUser = user;
                return service.currentUser;
            });
        }
        
        return $q.when(service.currentUser);
    };
    
    return service;
});