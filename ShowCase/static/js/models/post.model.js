angular.module('module.model')
.factory('postModel', ['$http', function ($http) {
	var service = {};
	service.getCompositionPosts = function (compositionId) {
		return $http.get('/compositions/' + compositionId + '/posts').then(function (response) {
			return response.data;
		});
	};

	service.getUserPosts = function (userId, page) {
		return $http.get('/users/' + userId + '/posts?page='+page).then(function (response) {
			return response.data;
		});
	};

	service.addComment = function (postId, comment) {
		var commentUrl = "/posts/" + postId + "/comments"
		return $http.post(commentUrl, {"comment": comment}).then(function (response) {
			return response.data;
		});
	};

	service.getComments = function (postId) {
		var commentUrl = "/posts/" + postId + "/comments"
		return $http.get(commentUrl).then(function (response) {
			return response.data;
		});
	};

	service.vote = function (postId, vote) {
		var voteUrl = "/posts/" + postId + "/votes"
		return $http.post(voteUrl, {vote: vote}).then(function (response) {
			return response.data;
		});
	};

	return service;
}]);