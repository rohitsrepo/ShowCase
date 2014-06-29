var collectionModule = angular.module('controller.collection', ['artifact.bookmark']);

collectionModule.controller('collectionCtrl', ['$scope', 'bookmarkFactory', function ($scope, bookmarkFactory) {
    'use strict';
    // TODO get this user from the parent.
    $scope.currentUser = {first_name: 'Rohit', id: 1};
    bookmarkFactory.getBookmark($scope.currentUser.id).then(function (res) {
        $scope.compositions = res;
    }, function () {});
    
    $scope.remove = function (compositionIndex) {
        var composition = $scope.compositions[compositionIndex];
        bookmarkFactory.deleteBookmark($scope.currentUser.id, composition.id).then(function (res) {
            $scope.compositions.splice(compositionIndex, 1);
        }, function (res) {});
    };
    
}]);