angular.module("CompositionApp").
controller("compositionController", ["$scope", "interpretationModel", '$location' ,function ($scope, interpretationModel, $location) {

	$scope.$watch($scope.compositionId, function () {
		interpretationModel.getInterpretations($scope.compositionId).then(function (interpretations) {
			$scope.interpretations = interpretations;
			console.log("got: ", interpretations);
		})		
	})
}]);