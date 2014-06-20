var showcaseModule = angular.module('showcaseApp', ['ui.router', 'security.service', 'controller.index']);

showcaseModule.config(function ($httpProvider, $stateProvider, $urlRouterProvider) {
    'use strict';
    
    $urlRouterProvider.otherwise('/popular');
    
    $stateProvider.state('reader', {
        url: '/popular',
        templateUrl: 'static/partials/reader.html',
        controller: 'readerCtrl'
    }).state('composition', {
        url: '/compositions/:compositionId/:slug',
        templateUrl: '/static/partials/composition.html',
        controller: 'compositionCtrl'
    }).state('test', {
        url: '/test',
        templateUrl: '/static/partials/test.html',
        controller: 'testCtrl'
    });
    
    // csrf for django 
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
});

showcaseModule.run(['securityFactory', function (securityFactory) {
    'use strict';
    
    // Fetch the logged in user from last session before
    // start of applicaiton.
    
    securityFactory.getCurrentUser();
}]);