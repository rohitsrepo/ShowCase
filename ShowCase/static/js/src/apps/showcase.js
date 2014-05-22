var showcaseModule = angular.module('showcaseApp', ['controller.reader']);

showcaseModule.config(function ($httpProvider) {
    'use strict';
    
    /* csrf for django */
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
});