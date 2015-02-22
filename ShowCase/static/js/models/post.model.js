angular.module("module.model")
.factory("posts", ['$http', function ($http) {

	var service = {};
	service.getPosts = function (pageNum) {
		return $http.get('/feeds/editors?page='+pageNum).then(function (response) {
			return response.data;
		});
	};

	return service;
}]);