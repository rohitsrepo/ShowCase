var authModule = angular.module('authModule', []);

authModule.factory('authService', function ($http) {
    var authService= {};
    authService.getCurrentUser = function () {
        return $http({withCredentials: true, method: 'GET', url: 'users/currentUser.json'});
    }();
    return authService;
});
