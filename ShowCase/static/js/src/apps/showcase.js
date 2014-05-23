var showcaseModule = angular.module('showcaseApp', ['controller.reader', 'controller.composition', 'ui.router']);

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
    
    /* csrf for django */
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
});