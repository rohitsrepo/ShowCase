angular.module('module.model')
.factory('postModel', ['$http', '$q', function ($http, $q) {
	var service = {};
	service.getCompositionPosts = function (compositionId) {
		return $http.get('/compositions/' + compositionId + '/posts').then(function (response) {
			return response.data;
		}, function (response) {
            return $q.reject(response);
        });
	};

	service.getUserPosts = function (userId, page) {
		return $http.get('/users/' + userId + '/posts?page='+page).then(function (response) {
			return response.data;
		}, function (response) {
            return $q.reject(response);
        });
	};

	service.addComment = function (postId, comment) {
		var commentUrl = "/posts/" + postId + "/comments"
		return $http.post(commentUrl, {"comment": comment}).then(function (response) {
			return response.data;
		}, function (response) {
            return $q.reject(response);
        });
	};

	service.getComments = function (postId) {
		var commentUrl = "/posts/" + postId + "/comments"
		return $http.get(commentUrl).then(function (response) {
			return response.data;
		}, function (response) {
            return $q.reject(response);
        });
	};

	service.vote = function (postId, vote) {
		var voteUrl = "/posts/" + postId + "/votes"
		return $http.post(voteUrl, {vote: vote}).then(function (response) {
			return response.data;
		}, function (response) {
            return $q.reject(response);
        });
	};

    service.getPost = function (userId, postId) {
        return $http.get('/users/' + userId + '/posts/' + postId).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

	return service;
}]);