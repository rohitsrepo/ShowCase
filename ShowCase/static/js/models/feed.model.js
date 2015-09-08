angular.module("module.model")
.factory("feedModel", ['$http', function ($http) {

	var DefaultFeed = 'editors';

	var validateFeed = function (feedName) {
		if (feedName!=='editors') {
			return DefaultFeed;
		}

		return feedName;
	};

	var service = {};
	service.getPosts = function (pageNum) {
		return $http.get('/feeds/editors?page='+pageNum).then(function (response) {
			return response.data;
		}, function (response) {
            return $q.reject(response);
        });
	};

	service.nextPosts = function (feedName, postId, compositionId) {
		var feed = validateFeed(feedName)
		return $http.get('/feeds/'+ feed +'/next?postId=' + postId + '&compositionId=' + compositionId)
		.then(function (response) {
			return response.data;
		}, function (response) {
            return $q.reject(response);
        });
	};

    service.getFresh = function (pageNum) {
        return $http.get('/feeds/fresh?page='+pageNum).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };


	return service;
}]);