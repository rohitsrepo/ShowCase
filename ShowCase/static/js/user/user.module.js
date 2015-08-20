angular.module("UserApp", [
    "lr.upload",
    'ui.router',
    "module.root"])
.config(['$httpProvider',
 '$interpolateProvider',
 '$stateProvider',
 '$urlRouterProvider',
 '$locationProvider',
  function ($httpProvider, $interpolateProvider, $stateProvider, $urlRouterProvider, $locationProvider) {
    "use strict";

    // Changing angular template tag to prevent conflict with django
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]')

    //Http Intercpetor to check auth failures for xhr requests
    $httpProvider.interceptors.push('authHttpResponseInterceptor');

    // csrf for django
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';

    // use the HTML5 History API
    $locationProvider.html5Mode(true);

    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/paintings");
    //
    // Now set up the states
    $stateProvider
    .state('activities', {
        url: "/activities",
        templateUrl: "/static/js/user/profile.activities.html",
        controller: 'profileActivitiesController'
    })
    .state('paintings', {
        url: "/paintings",
        templateUrl: "/static/js/user/profile.paintings.html",
        controller: 'profilePaintingsController',
        data: {'listType': 'paintings'}
    })
    .state('uploads', {
        url: "/uploads",
        templateUrl: "/static/js/user/profile.paintings.html",
        controller: 'profilePaintingsController',
        data: {'listType': 'uploads'}
    })
    .state('bookmarks', {
        url: "/admirations",
        templateUrl: "/static/js/user/profile.paintings.html",
        controller: 'profilePaintingsController',
        data: {'listType': 'bookmarks'}
    })
    .state('buckets', {
        url: "/series",
        templateUrl: "/static/js/user/profile.buckets.html",
        controller: 'profileBucketsController'
    });
}]).factory('authHttpResponseInterceptor', ['$q', '$window', function ($q, $window) {
    'use strict';
    return {
        responseError: function (response) {
            if (response.status === 403) {
                $window.location.href = "/login#?next=" + $window.location.pathname;
            }
            return $q.reject(response);
        }
    };
}]).run(['auth', '$window', function (auth, $window) {
    auth.getCurrentUser();
}]);