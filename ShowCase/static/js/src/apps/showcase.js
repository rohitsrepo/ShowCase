var showcaseModule = angular.module('showcaseApp', ['controller.reader', 'controller.composition', 'ui.router', 'security.service', 'controller.navbarTop']);

showcaseModule.config(function ($httpProvider, $stateProvider, $urlRouterProvider) {
    'use strict';
    
    $urlRouterProvider.otherwise('/popular');
    
    $stateProvider.state('reader', {
        url: '/popular',
        templateUrl: 'static/partials/reader.html',
        controller: 'readerCtrl'
    }).state('composition', {
        url: '/compositions/:compositionId',
        templateUrl: '/static/partials/composition.html',
        controller: 'compositionCtrl'
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