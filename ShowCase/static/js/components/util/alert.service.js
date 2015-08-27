angular.module('module.util')
.factory('alert', ['$timeout', function ($timeout) {

	var service = {};

	service.show = false;
	service.content = 'Welcome';

	service.showAlert = function (content) {

		service.content = content;
		service.show = true;

		$timeout(function () {
			service.show = false;
		}, 4000);
	};

	return service;
}]);