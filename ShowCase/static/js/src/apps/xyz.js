var xyzModule = angular.module('showcaseApp', ['ui.router', 'security.service', 'controller.index']);

xyzModule.config(function ($httpProvider, $stateProvider, $urlRouterProvider) {
    'use strict';
    
    //Http Intercpetor to check auth failures for xhr requests
    $httpProvider.interceptors.push('authHttpResponseInterceptor');
    
    $urlRouterProvider.otherwise('/popular');
    
    $stateProvider.state('reader', {
        url: '/popular',
        templateUrl: 'static/partials/reader.html',
        controller: 'readerCtrl'
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
    }).state('test', {
        url: '/test',
        templateUrl: '/static/partials/test.html',
        controller: 'testCtrl'
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

xyzModule.factory('authHttpResponseInterceptor', ['$q', '$window', function ($q, $window) {
    'use strict';
    
    var loginPrompt = function () {
        if (confirm('Do you wish to login mate!!!')) {
            $window.location.href = '/usersapi-auth/login/';
        }
    };
    
    return {
        response: function (response) {
            if (response.status === 401) {
                console.log("Response 401");
            }
            return response || $q.when(response);
        },
        responseError: function (rejection) {
            if (rejection.status === 401) {
                console.log("Response Error 401", rejection);
                //$location.path('/login').search('returnTo', $location.path());
            }
            return $q.reject(rejection);
        }
    };
}]);