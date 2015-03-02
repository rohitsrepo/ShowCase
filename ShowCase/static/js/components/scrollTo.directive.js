angular.module("module.scrollTo", [])
.directive('scrollTo', [function () {
	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			element.bind('click', function () {
				var scrollTo = $(attrs['scrollTo']).offset().top;
				$('html,body').animate({
			        'scrollTop': scrollTo
			    }, 750);
			});
		}
	};
}]);