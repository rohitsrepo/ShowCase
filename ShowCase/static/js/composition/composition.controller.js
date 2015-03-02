angular.module("CompositionApp").
controller("compositionController", ["$scope", "interpretationModel", '$location' , '$timeout', 
	function ($scope, interpretationModel, $location, $timeout) {

	$scope.composition = {};

	$scope.init = function (id, url) {
		$scope.composition.id = id;
		$scope.composition.url = url;
	};

	var checkForScroll = function (interval) {
		$timeout (function () {
			var scrollTo = $location.search()['scrollTo'];
			console.log("got", scrollTo);
			if (scrollTo) {
				var elementTop = $('#'+scrollTo).offset().top;
				$('html,body').animate({
			        'scrollTop': elementTop
			    }, 750);
			}
		}, interval)
		
	};


	$scope.$watch($scope.composition.Id, function () {
		interpretationModel.getInterpretations($scope.composition.id).then(function (interpretations) {
			$scope.interpretations = interpretations;
			checkForScroll(500);
		});
	});

	$scope.vote = function (index, vote) {
		interpretation = $scope.interpretations[index];
		interpretationModel.vote($scope.composition.id, interpretation.id, vote).then(function (response) {
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
		interpretationModel.addComment($scope.composition.id, interpretation.id, comment).then(function (res) {
			interpretation.comments.push(res);
			interpretation.comment = "";
		});
	};

	var getComments = function (index) {
		interpretation = $scope.interpretations[index];
		interpretationModel.getComments($scope.composition.id, interpretation.id).then(function (res) {
			interpretation.comments = res;
		});
	};


}]);