var compositionsApp = angular.module('compositionsApp', []);

compositionsApp.controller('CompostionListCtrl', function ($scope, $http) {
    $http({withCredentials: true, headers: {'Content-Type': 'application/json; charset=utf-8'}, metod: 'GET', url: 'compositions/.json'}).success(function (data) {
	$scope.compositions = data;
        
        $scope.currentComposition = $scope.compositions[0];
    
        $scope.showComposition = function (composition) {
            $scope.currentComposition = composition;
	};
    
        $scope.isActive = function (compositionID) {
            return compositionID === $scope.currentComposition.id;
        };

    });
    
});
