angular.module('module.alert', [])
.factory('alert', ['$timeout', function ($timeout) {

	var service = {};
	service.meta = {'show': false, 'content': false};

	service.showAlert = function (content) {
		service.meta.content = content;
		service.meta.show = true;

		$timeout(function () {
			service.meta.show = false;
		}, 4000);
	};

	return service;
}]);