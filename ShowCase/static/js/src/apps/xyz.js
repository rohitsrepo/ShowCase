var xyzModule = angular.module('showcaseApp', ['ui.router', 'security.service', 'controller.index', 'ui.utils']);

xyzModule.config(function ($httpProvider, $stateProvider, $urlRouterProvider) {
    'use strict';
    
    //Http Intercpetor to check auth failures for xhr requests
    $httpProvider.interceptors.push('authHttpResponseInterceptor');
    
    $urlRouterProvider.otherwise('/popular');
    
    $stateProvider.state('reader', {
        url: '/popular',
        templateUrl: 'static/partials/reader.html',
        controller: 'readerCtrl'
    }).state('test', {
        url: '/test',
        templateUrl: '/static/partials/test.html',
        controller: 'testCtrl'
    }).state('composition', {
        url: '/compositions/:compositionId/:slug',
        templateUrl: '/static/partials/composition.html',
        controller: 'compositionCtrl'
    }).state('showcase', {
        url: '/:userId',
        templateUrl: '/static/partials/showcase.html',
        controller: 'showcaseCtrl',
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
        templateUrl: '/static/partials/collection.html',
        controller: 'collectionCtrl'
    }).state('showcase.follow', {
        url: '/follow',
        templateUrl: '/static/partials/follow.html',
        controller: 'followCtrl'
    }).state('showcase.notifications', {
        url: '/notifications',
        templateUrl: '/static/partials/notification.html',
        controller: 'notificationCtrl'
    });
    
    // csrf for django 
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
});

xyzModule.run(['securityFactory', function (securityFactory) {
    'use strict';
    
    // Fetch the logged in user from last session before
    // start of applicaiton.
    
    securityFactory.getCurrentUser();
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