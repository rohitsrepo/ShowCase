angular.module('module.scrollTo')
.directive('fadeOnScroll', ['$document', '$timeout', function ($document, $timeout) {
	var state = "show";

	function showElement(element) {
		if (element.hasClass('fadeOut')){
            element.removeClass('animated fadeOut');
            element.addClass('animated fadeIn');
        }
        element.show();
	};

	function hideElement(element) {
		element.removeClass('animated fadeIn');
        element.addClass('animated fadeOut');
        $timeout(function () {
        	element.hide();
        }, 300);
	};

	

	return function(scope, element, attrs) {

		scope.$watch(function () {
			return state;
		}, function (newVal) {
			if (newVal=="hide"){
				hideElement(element);
			} else {
				showElement(element);
			}
		});

        $document.bind('scroll', function () {
            if ($document.scrollTop() < 100) {
		        state = "show";
            } else {
            	state = "hide";
            }
	         scope.$apply();
        });
	};
}]);