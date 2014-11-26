var collectionModule = angular.module('collection.module', ['artifact.bookmark']);

collectionModule.controller('collectionController', ['$scope', 'bookmarkFactory', '$log', 'getUser', function ($scope, bookmarkFactory, $log, getUser) {
    'use strict';
    // TODO get this user from the parent.
    $scope.user = getUser;
    bookmarkFactory.getBookmark($scope.user.id).then(function (res) {
        $scope.compositions = res;
    }, function () {});
    
    $scope.remove = function (compositionIndex) {
        var composition = $scope.compositions[compositionIndex];
        bookmarkFactory.deleteBookmark($scope.user.id, composition.id).then(function (res) {
            $scope.compositions.splice(compositionIndex, 1);
        }, function (res) {});
    };
    
}]);