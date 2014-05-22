var loggerModule = angular.module('helper.logger', []);

loggerModule.factory('logger', function () {
    'use strict';
    
    return function (prefText, data) {
        console.log('Logging from ' + prefText + '...');
        console.log(data);
        console.log('...|');
    };
});