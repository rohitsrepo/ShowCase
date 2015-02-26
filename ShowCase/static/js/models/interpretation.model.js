angular.module('module.model')
.factory('interpretationModel', ['$http', function ($http) {
	var service = {};
	service.getInterpretations = function (compositionId) {
		return $http.get('/compositions/' + compositionId + '/interpretations').then(function (response) {
			return response.data;
		});
	};
	return service;
}]);