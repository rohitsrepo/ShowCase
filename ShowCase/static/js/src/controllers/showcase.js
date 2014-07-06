var showcaseModule = angular.module('controller.showcase', ['artifact.composition']);

showcaseModule.controller('showcaseCtrl', ['$scope', 'compositionFactory', 'getUser',  function ($scope, compositionFactory, getUser) {
    'use strict';
    
    $scope.currentUser = getUser;
    $scope.compositions = compositionFactory.manager.query({artist: getUser.id});
}]);