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
}])
.directive('analyticsScroll', ['analytics', '$document', function (analytics, $document) {
	return {
		restrict: 'A',
		scope: {
			analyticsData: '=',
			analyticsOffset: '='
		},
		link: function (scope, elem, attrs) {
			var doItOnce = true;
			var offset = scope.analyticsOffset || 250;
			var scrollTop, topMark;

			$document.bind('scroll', function () {
				if (doItOnce){
					scrollTop = $document.scrollTop();
					topMark = elem.offset().top;

					if (scrollTop > topMark - offset){
						analytics.logEvent.apply(this, scope.analyticsData);
						doItOnce = false;
					}
				}
			});
		}
	};
}]);