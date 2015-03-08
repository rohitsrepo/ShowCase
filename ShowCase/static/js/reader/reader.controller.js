angular.module("ReaderApp")
.controller("readerController", ["$scope", 'posts', 'interpretationModel', function ($scope, posts, interpretationModel) {
	"use strict";

	posts.getPosts().then(function (posts) {
		$scope.posts = posts.results
	});

	$scope.showInterpretation = function (index) {
		$scope.posts[index].showComplete = true;
	};

	$scope.vote = function (index, vote) {
		var post = $scope.posts[index];
		interpretationModel.vote(post.composition.id, post.interpretation.id, vote).then(function (response) {
			post.interpretation.vote.total = response.total;
			post.voting_status = vote ? "Positive" : "Negative";
		});
	};

}]);