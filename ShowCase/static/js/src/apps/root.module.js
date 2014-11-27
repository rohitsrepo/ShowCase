var xyzModule = angular.module('showcaseApp', ['ui.router', 'authentication', 'controller.index', 'ui.utils', 'reader.module', 'composition.module', 'collection.module', 'follow.module', 'notification.module', 'showcase.module']);

xyzModule.config(function ($httpProvider, $stateProvider, $urlRouterProvider) {
    'use strict';
    
    //Http Intercpetor to check auth failures for xhr requests
    $httpProvider.interceptors.push('authHttpResponseInterceptor');
    
    $urlRouterProvider.otherwise('/popular');
    
    $stateProvider.state('reader', {
        url: '/popular',
        templateUrl: 'static/js/src/apps/reader/reader.html',
        controller: 'readerController'
    }).state('composition', {
        url: '/compositions/:compositionId/:slug',
        templateUrl: '/static/js/src/apps/composition/composition.html',
        controller: 'compositionController'
    }).state('showcase', {
        url: '/:userId',
        templateUrl: '/static/js/src/apps/showcase/showcase.html',
        controller: 'showcaseController',
        resolve: {
            getUser: function ($stateParams, userFactory) {
                return userFactory.getUser($stateParams.userId).then(function (res) {
                    return res.data;
                });
                //return userFactory.getUser.get({userId: $stateParams.userId}, function (res) {return res;} );
            }
        }
    }).state('showcase.collection', {
        url: '/collection',
        templateUrl: '/static/js/src/apps/collection/collection.html',
        controller: 'collectionController'
    }).state('showcase.follow', {
        url: '/follow',
        templateUrl: '/static/js/src/apps/follow/follow.html',
        controller: 'followController'
    }).state('showcase.notifications', {
        url: '/notifications',
        templateUrl: '/static/js/src/apps/components/notification/notification.html',
        controller: 'notificationController'
    }).state('test', {
        url: '/test',
        templateUrl: '/static/partials/test.html',
        controller: 'testCtrl'
    });
    
    // csrf for django 
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
});

xyzModule.run(['authenticationService', function (authenticationService) {
    'use strict';
    
    // Fetch the logged in user from last session before
    // start of applicaiton.
    
    authenticationService.getCurrentUser();
}]);

xyzModule.factory('authHttpResponseInterceptor', ['$q', '$window', '$log', function ($q, $window, $log) {
    'use strict';
    
    var loginPrompt = function () {
        if (confirm('Do you wish to login mate!!!')) {
            $window.location.href = '/usersapi-auth/login/';
        }
    };
    
    return {
        response: function (response) {
            if (response.status === 401) {
                $log.info("Interceptor: Response 401");
            }
            return response || $q.when(response);
        },
        responseError: function (rejection) {
            if (rejection.status === 401) {
                $log.info("Interceptor: Response Error 401", rejection);
                //$location.path('/login').search('returnTo', $location.path());
            }
            return $q.reject(rejection);
        }
    };
}]);