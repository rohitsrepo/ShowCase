angular.module('module.util', [])
.directive('headerScroll', ['$window', '$interval', function ($window, $interval) {
	return function(scope, element, attrs) {
	    var didScroll;
	    var lastScrollTop = 0;
	    var delta = 5;
	    var navbarHeight = element.outerHeight();

	    $(window).scroll(function(event){
	        didScroll = true;
	    });

	    $interval(function() {
	        if (didScroll) {
	            hasScrolled();
	            didScroll = false;
	        }
	    }, 250);

	    function hasScrolled() {
	        var st = $(this).scrollTop();
	        
	        // Make sure they scroll more than delta
	        if(Math.abs(lastScrollTop - st) <= delta)
	            return;
	        
	        // If they scrolled down and are past the navbar, add class .nav-up.
	        // This is necessary so you never see what is "behind" the navbar.
	        if (st > lastScrollTop && st > navbarHeight){
	            // Scroll Down
	            element.addClass('header-pull-up');
	        } else {
	            // Scroll Up
	            if(st + $(window).height() < $(document).height()) {
	                element.removeClass('header-pull-up');
	            }
	        }
	        
	        lastScrollTop = st;
	    }
	};
}]);