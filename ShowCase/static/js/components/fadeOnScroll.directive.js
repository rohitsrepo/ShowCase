angular.module('module.scrollTo')
.directive('fadeOnScroll', ['$document', function ($document) {
	return function(scope, element, attrs) {
           element.addClass('animated fadeIn');
	       $document.bind('scroll', function () {
	           if ($document.scrollTop() < 100) {
		           element.removeClass('animated fadeOut');
		           element.addClass('animated fadeIn');
		           element.show();
	           } else {
		           element.removeClass('animated fadeIn');
		           element.addClass('animated fadeOut');
		           element.hide();
	           }
	       });
	   };
}]);