angular.module("CompositionApp").
controller("compositionController", ["$scope", "interpretationModel", '$location' ,function ($scope, interpretationModel, $location) {

	$scope.$watch($scope.compositionId, function () {
		interpretationModel.getInterpretations($scope.compositionId).then(function (interpretations) {
			$scope.interpretations = interpretations;
		});
	});

	$scope.vote = function (index, vote) {
		interpretation = $scope.interpretations[index];
		interpretationModel.vote($scope.compositionId, interpretation.id, vote).then(function (response) {
			interpretation.vote.total = response.total;
			interpretation.voting_status = vote ? "Positive" : "Negative";
		});
	};

	$scope.toggleShowComments = function (index) {
		var interpretation = $scope.interpretations[index];
		interpretation.showComments = !interpretation.showComments;
		if (interpretation.showComments) {
			getComments(index);
		};
	};

	$scope.addComment = function (index, comment) {
		interpretation = $scope.interpretations[index];
		interpretationModel.addComment($scope.compositionId, interpretation.id, comment).then(function (res) {
			console.log("controller: ", res);
			interpretation.comments.push(res);
			interpretation.comment = "";
		});
	};

	var getComments = function (index) {
		interpretation = $scope.interpretations[index];
		interpretationModel.getComments($scope.compositionId, interpretation.id).then(function (res) {
			console.log("controller got", res);
			interpretation.comments = res;
		});
	};


}]);