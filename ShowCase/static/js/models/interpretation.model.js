angular.module('module.model')
.factory('interpretationModel', ['$http', '$q', function ($http, $q) {
	var service = {};

    service.addInterpretation = function (compositionId, interpretation) {
        var interpretUrl = "/compositions/" + compositionId + "/interpretations";
        return $http.post(interpretUrl, {"interpretation": interpretation}).then(function (response) {
            return response.data;
        });
    };

    service.artInterprets = function (compositionId) {
        var interpretUrl = "/compositions/" + compositionId + "/interprets";
        return $http.get(interpretUrl).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

	return service;
}]);