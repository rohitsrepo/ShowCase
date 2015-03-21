angular.module("module.model")
.factory("contentManager", ['$http', function ($http) {

	var service = {};
	service.reportComposition = function (compositionId) {
		return $http.post('/content/report', data={'compositionId': compositionId}).then(function (response) {
			return response.data;
		});
	};

	return service;
}]);