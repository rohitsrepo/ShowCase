angular.module('module.model')
.factory('interpretationModel', ['$http', function ($http) {
	var service = {};
	service.getInterpretations = function (compositionId) {
		return $http.get('/compositions/' + compositionId + '/interpretations').then(function (response) {
			return response.data;
		});
	};

	service.vote = function (compositionId, interpretationId, vote) {
		var voteUrl = "/compositions/" + compositionId + "/interpretations/" + interpretationId + "/votes"
		return $http.post(voteUrl, {vote: vote}).then(function (response) {
			return response.data;
		});
	};
	return service;
}]);