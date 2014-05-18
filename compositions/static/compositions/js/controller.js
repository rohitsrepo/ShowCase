var compositionsApp = angular.module('compositionsApp', ['authModule', 'compositionService']);

compositionsApp.controller('CompostionListCtrl', function ($scope, $http, authService, Compositions) {
    $scope.newComment = '';
    
    $scope.compositions = Compositions.manager.query(function (data) {
        //$scope.currentComposition = $scope.compositions[0];
        $scope.showComposition($scope.compositions[0]);
    });
    
    $scope.showComposition = function (composition) {
        $scope.currentComposition = composition;
        Compositions.votes.get(composition.id).then(function (res) {
            $scope.vote = res.data;
        }, function (res) {
            //TODO handle error according to status of error.
            // Global exception handling.
            console.log("error while getting votes.");
            console.log(res);
        });
        
        $scope.comments = Compositions.comments.query({compositionId: composition.id});
    };
    
    $scope.isActive = function (compositionID) {
        return compositionID === $scope.currentComposition.id;
    };
    authService.getCurrentUser.then(function (res) {
        $scope.currentUser = res.data;
    }, function (res) {
            //TODO handle error according to status of error.
            // Global exception handling.        
        $scope.currentUser = '';
    });
    
    $scope.deleteComposition = function (composition) {
        Compositions.manager.delete({compositionId: $scope.currentComposition.id});
    };
    
    $scope.voting = function (vote) {
        Compositions.votes.put($scope.currentComposition.id, vote).then(function (res) {
            $scope.vote = res.data;
        }, function (res) {
            //TODO handle error according to status of error.
            // Global exception handling.
            console.log("error while putting votes.");
            console.log(res);
        });
    };
    
    $scope.commenting = function () {
        var res = Compositions.comments.save({compositionId: $scope.currentComposition.id}, {comment: $scope.newComment}, function (res) {
            $scope.comments = Compositions.comments.query({compositionId: $scope.currentComposition.id});
            $scope.newComment = '';
        });
        
    };
});