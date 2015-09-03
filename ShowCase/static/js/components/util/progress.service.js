angular.module('module.util')
.factory('progress', ['$timeout', '$interval', function ($timeout, $interval) {
	var intervalPromise;
    var activeCount = 0;

	var animate = function () {
		$('.progress-bar').addClass('animate');

		$timeout(function () {
			$('.progress-bar').removeClass('animate');
		}, 2100);
	};

	var service = {};

	service.showProgress = function () {
        if (!activeCount) {
    		animate();
    		intervalPromise = $interval(function () {
    			animate();
    		}, 2200);
        }

        activeCount++;
	}

	service.hideProgress = function () {
        activeCount--;

        if (!activeCount) {
		 $interval.cancel(intervalPromise);
        }
	};

	return service;
}]);