var securityModule = angular.module('security.service', ['artifact.user', 'ui.bootstrap', 'ui.router']);

securityModule.factory('securityFactory', ['$http', '$q', 'userFactory', '$modal', '$state', function ($http, $q, userFactory, $modal, $state) {
    'use strict';
    
    var loginModal, service = {};
    
    service.currentUser = null;
    service.redirectState = '';
                                           
    service.redirect = function (state) {
        state = state || 'reader';
        $state.go(state);
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
        return $http({method: 'POST',
                      url: '/users/login',
                      data: {email: email, password: password}
                     }).then(function (res) {
            service.currentUser = res.data;
            return service.isAuthenticated();
        }, function (res) {
            console.log('Error', res);
        });
    };
    
    service.logout = function () {
        return $http({method: 'GET',
                      url: '/users/logout'
                     }).then(function (res) {
            service.currentUser = '';
        }, function (res) {
            console.log('Error', res);
        });
    };
    
    service.showLoginModal = function () {
        service.redirectState = $state.current.name;
        loginModal = $modal.open({
            templateUrl: '/static/partials/login.html',
            controller: 'loginCtrl'
        });
        
        loginModal.result.then(function (result) {
            //retry requests/Redirect.
            service.redirect(service.redirectState);
        }, function (result) {
            console.info('Log In cancelled.');
        });
    };
    
    service.checkForAuth = function () {
        if (!service.isAuthenticated()) {
            service.showLoginModal();
            return false;
        }
        return true;
    };
                                 
    return service;
}]);