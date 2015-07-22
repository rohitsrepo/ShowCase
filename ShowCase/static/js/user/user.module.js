angular.module("UserApp", [
    'infinite-scroll',
    "lr.upload",
    'ngAnimate',
    'ui.router',
    "module.auth",
    "module.topbar",
    "module.model",
    'module.titlecase',
    'module.scrollTo',
    'module.util',
    'module.analytics'])
.config(['$httpProvider', '$interpolateProvider', '$stateProvider', '$urlRouterProvider', function ($httpProvider, $interpolateProvider, $stateProvider, $urlRouterProvider) {
    "use strict";

    // Changing angular template tag to prevent conflict with django
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]')

    //Http Intercpetor to check auth failures for xhr requests
    $httpProvider.interceptors.push('authHttpResponseInterceptor');

    // csrf for django
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';

    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/paintings");
    //
    // Now set up the states
    $stateProvider
      .state('paintings', {
        url: "/paintings",
        templateUrl: "/static/js/user/profile.paintings.html",
        controller: 'profilePaintingsController'
    })
    .state('uploads', {
        url: "/uploads",
        templateUrl: "/static/js/user/profile.uploads.html",
        controller: 'profileUploadsController'
    })
    .state('interpretations', {
        url: "/interpretations",
        templateUrl: "/static/js/user/profile.interpretations.html",
        controller: 'profilePostsController'
    })
    .state('collection', {
        url: "/collection",
        templateUrl: "/static/js/user/profile.collection.html",
        controller: 'profileCollectionController'
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