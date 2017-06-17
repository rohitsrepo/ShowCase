angular.module('module.model')
.factory('interpretationModel', ['$http', '$q', function ($http, $q) {
	var service = {};

    service.addInterpretation = function (interpretation_id, title, interpretation, isDraft) {
        var interpretUrl = "/interpretations/" + interpretation_id;
        return $http.put(interpretUrl, {"title": title, "interpretation": interpretation, 'is_draft': isDraft}).then(function (response) {
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

    service.getRelated = function (interpretationId) {
        var interpretUrl = "/interpretations/" + interpretationId + "/related";
        return $http.get(interpretUrl).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

	return service;
}]);