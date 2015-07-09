angular.module('module.model')
.factory('interpretationModel', ['$http', function ($http) {
	var service = {};

	service.vote = function (compositionId, interpretationId, vote) {
		var voteUrl = "/compositions/" + compositionId + "/interpretations/" + interpretationId + "/votes"
		return $http.post(voteUrl, {vote: vote}).then(function (response) {
			return response.data;
		});
	};

	service.addComment = function (compositionId, interpretationId, comment) {
		var commentUrl = "/compositions/" + compositionId + "/interpretations/" + interpretationId + "/comments"
		return $http.post(commentUrl, {"comment": comment}).then(function (response) {
			return response.data;
		});
	};

	service.addInterpretation = function (compositionId, interpretation) {
		var interpretUrl = "/compositions/" + compositionId + "/interpretations";
		return $http.post(interpretUrl, {"interpretation": interpretation}).then(function (response) {
			return response.data;
		});
	}

	return service;
}]);