angular.module("ReaderApp")
.controller("readerController", ["$scope",
 'posts',
 'interpretationModel',
 'analytics',
 function ($scope,
 	posts,
 	interpretationModel,
 	analytics)
 {
	"use strict";
	$scope.postsMeta = {pageVal: 1, disableGetMore: false, busy: false};
	$scope.posts = [];

	var getPosts = function () {

		if (!$scope.postsMeta.disableGetMore) {
			var pageVal = $scope.postsMeta.pageVal;
			posts.getPosts(pageVal).then(function (posts) {

				for (var i = 0; i < posts.results.length; i++) {
			    	$scope.posts.push(posts.results[i]);
			    }

				if (posts.next == null){
					$scope.postsMeta.disableGetMore = true;
					analytics.logEvent('Reader', 'scroll', 'Load More Posts - Hit Bottom', $scope.posts.length);
				}

				$scope.postsMeta.busy = false;
			});
		}

		$scope.postsMeta.pageVal += 1;
	}

	$scope.loadMorePosts = function () {
		if ($scope.postsMeta.busy) {
			return;
		}
		
		$scope.postsMeta.busy = true;
		getPosts($scope.postsMeta);
		analytics.logEvent('Reader', 'scroll', 'Load More Posts', $scope.posts.length);
	};

	$scope.vote = function (index, vote) {
		var post = $scope.posts[index];
		analytics.logEvent('Reader', 'click', 'vote');
		interpretationModel.vote(post.composition.id, post.interpretation.id, vote).then(function (response) {
			post.interpretation.vote.total = response.total;
			post.voting_status = vote ? "Positive" : "Negative";
		});
	};

}]);