angular.module('module.analytics')
.directive('analyticsClick', ['analytics', function (analytics) {
	return {
		restrict: 'A',
		scope: {
			analyticsData: '='
		},
		link: function (scope, elem, attrs) {
			elem.bind('click', function () {
				analytics.logEvent.apply(this, scope.analyticsData);
			});
		}
	};
}]);