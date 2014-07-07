var registerModule = angular.module('service.register', ['ui.bootstrap', 'ui.router', 'security.service']);

registerModule.factory('registerFactory', ['$modal', '$log', '$state', 'securityFactory', '$window', function ($modal, $log, $state, securityFactory, $window) {
    'use strict';
    
    var service = {};
    service.registerModal = null;
    service.showRegisterModal = function () {
        service.registerModal = $modal.open({
            templateUrl: '/static/partials/registerModal.html',
            controller: 'registerModalCtrl',
            size: 'lg'
        });
        
        service.registerModal.result.then(function (result) {
            //retry requests/Redirect.
            $state.go('reader');
            if (result.response.status === 201) {
                $log.info('The modal returned.', result);
                securityFactory.login(result.user.email, result.user.password).then(function (res) {
                    $window.location.reload();
                }, function (res) {
                    $log.error('Log-In user after registration:', res);
                });
            }
        }, function (result) {
            $log.info('Registration cancelled.');
        });
    };
    
    return service;
}]);