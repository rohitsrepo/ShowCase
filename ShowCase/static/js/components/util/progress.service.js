angular.module('module.util')
.factory('progress', ['$timeout', '$interval', function ($timeout, $interval) {
	var intervalPromise;

	var animate = function () {
		$('.progress-bar').addClass('animate');

		$timeout(function () {
			$('.progress-bar').removeClass('animate');
		}, 2100);
	};

	var service = {};

	service.showProgress = function () {
		animate();
		intervalPromise = $interval(function () {
			animate();
		}, 2200);
	}

	service.hideProgress = function () {
		 $interval.cancel(intervalPromise);
	};

	return service;
}]);