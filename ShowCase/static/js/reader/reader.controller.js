angular.module("ReaderApp")
.controller("readerController", ["$scope",
 'posts',
 'interpretationModel',
 'analytics',
 '$location',
 function ($scope,
 	posts,
 	interpretationModel,
 	analytics,
 	$location)
 {
	"use strict";
	$scope.postsMeta = {pageVal: 1, disableGetMore: false, busy: false, next:'', previous:''};
	$scope.posts = [];

	function checkForPageValue() {
		var page = $location.search()['page'];
		page = parseInt(page);

		if(!isNaN(page)){
			$scope.postsMeta.pageVal = page;
		}
	};
	checkForPageValue();

	var getPosts = function () {

		if (!$scope.postsMeta.disableGetMore) {
			var pageVal = $scope.postsMeta.pageVal;
			posts.getPosts(pageVal).then(function (posts) {
				$scope.postsMeta.next = posts.next;
				$scope.postsMeta.previous = posts.previous;

				for (var i = 0; i < posts.results.length; i++) {
			    	$scope.posts.push(posts.results[i]);
			    }

				if (posts.next == null){
					$scope.postsMeta.disableGetMore = true;
					analytics.logEvent('Reader', 'Load More Posts - Hit Bottom');
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
		if ($scope.posts.length != 0){
			analytics.logEvent('Reader', 'Load More Posts');
		} else {
			analytics.logEvent('Reader', 'Init');
		}
		getPosts();
	};

	$scope.vote = function (index, vote) {
		var post = $scope.posts[index];
		analytics.logEvent('Reader', 'Feed-Comment-Click', post.composition.slug);
		interpretationModel.vote(post.composition.id, post.interpretation.id, vote).then(function (response) {
			post.interpretation.vote.total = response.total;
			post.voting_status = vote ? "Positive" : "Negative";
		});
	};

}]);