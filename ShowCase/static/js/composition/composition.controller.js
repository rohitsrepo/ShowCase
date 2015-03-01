angular.module("CompositionApp").
controller("compositionController", ["$scope", "interpretationModel", '$location' ,function ($scope, interpretationModel, $location) {

	$scope.$watch($scope.compositionId, function () {
		interpretationModel.getInterpretations($scope.compositionId).then(function (interpretations) {
			$scope.interpretations = interpretations;
		});
	});

	$scope.vote = function (index, vote) {
		interpretation = $scope.interpretations[index]
		interpretationModel.vote($scope.compositionId, interpretation.id, vote).then(function (response) {
			interpretation.vote.total = response.total;
			interpretation.voting_status = vote ? "Positive" : "Negative";
		});
	};

}]);