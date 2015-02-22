angular.module("ReaderApp")
.controller("readerController", ["$scope", 'posts', function ($scope, posts) {
	"use strict";

	posts.getPosts().then(function (posts) {
		$scope.posts = posts.results
	});

	$scope.showInterpretation = function (index) {
		$scope.posts[index].showComplete = true;
	};

}]);