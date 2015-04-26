angular.module('module.analytics', [])
.factory('analytics', [function () {
	var service = {};

	service.logEvent = function (category, action, label, value) {
		// ga('send', 'event', category, action, label, value);
	}

	return service;
}]);