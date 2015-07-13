angular.module('module.model')
.factory('interpretationModel', ['$http', function ($http) {
	var service = {};

	service.addInterpretation = function (compositionId, interpretation) {
		var interpretUrl = "/compositions/" + compositionId + "/interpretations";
		return $http.post(interpretUrl, {"interpretation": interpretation}).then(function (response) {
			return response.data;
		});
	}

	return service;
}]);