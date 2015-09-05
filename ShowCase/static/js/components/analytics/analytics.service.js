angular.module('module.analytics', [])
.factory('analytics', [function () {
	var service = {};

	service.logEvent = function (category, action, label, value) {
        if (document.location.hostname.search("thirddime.com") !== -1) {
    		ga('send', 'event', category, action, label, value);
        }
	}

	return service;
}]);