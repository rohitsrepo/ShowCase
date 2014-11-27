angular.module('authentication')
.factory('authenticationService', ['$http', '$q', 'userFactory', '$modal', '$state', '$log', '$window', function ($http, $q, userFactory, $modal, $state, $log, $window) {
    'use strict';
    
    var loginModal, service = {};
    
    service.currentUser = null;
    service.redirectState = '';
                                           
    service.redirect = function (state, force) {
        // No need felt for exposing redirection logic as all the states are AllowAny, block s w.r.t. to actions like voting so reloadin current state.
        //state = state || 'reader';
        if (force) {
            $log.info('We are here for force reload.');
            $window.location.reload();
        } else {
            $state.go($state.current.name, {location: 'replace'});
        }
    };
    
    service.getCurrentUser = function () {
        if (!service.currentUser) {
            return userFactory.getCurrentUser().then(function (user) {
                service.currentUser = user;
                return service.currentUser;
            });
        }
        return $q.when(service.currentUser);
    };
    
    service.isAuthenticated = function () {
        return !!(service.currentUser && service.currentUser.first_name);
    };
    
    service.login = function (email, password) {
        return userFactory.login(email, password).then(function (res) {
            service.currentUser = res.data;
            return service.isAuthenticated();
        }, function (res) {
            $log.error('Error', res);
        });
    };
    
    service.logout = function () {
        return userFactory.logout().then(function (res) {
            service.currentUser = '';
            service.redirect($state.current.name, true);
        }, function (res) {
            $log.error('Error', res);
        });
    };
    
    service.showLoginModal = function () {
        service.redirectState = $state.current.name;
        loginModal = $modal.open({
            templateUrl: '/static/js/src/apps/authentication/authentication.modal.html',
            controller: 'authenticationModalController'
        });
        
        /*return loginModal.result.then(function (result) {
            //retry requests/Redirect.
            service.redirect(service.redirectState);
            $log.info('form loginModal', result);
            return result;
        }, function (result) {
            $log.info('from login modal Log In cancelled.');
            $log.info('from loginModal', result);
            return result;
        });*/
        
        // Returning result promise so that user of the login modal can better handle situation on login/cancel.
        return loginModal.result;
    };
    
    service.checkForAuth = function () {
        if (!service.isAuthenticated()) {
            service.showLoginModal().then(function (res) {
                
                service.redirect($state.current.name, true);
            }, function (res) {
                $log.info('Login cancelled.');
            });
            return false;
        }
        return true;
    };
                                 
    return service;
}]);