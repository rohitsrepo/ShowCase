angular.module('module.util', [])
.directive('headerScroll', ['$window', '$interval', function ($window, $interval) {
	return function(scope, element, attrs) {
	    var didScroll;
	    var lastScrollTop = 0;
	    var delta = 5;
	    var navbarHeight = element.outerHeight();
	    var headerColor;

        var mq = window.matchMedia( "(max-width: 800px)" );

        if (mq.matches) {
            return;
        };

        headerColorInit();

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

	        headerColorOnScroll(headerColor, st);

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

	    function headerColorInit () {
	    	if (scope.headerColor){
	    		headerColor = hexToRgb(scope.headerColor);
	    		element[0].style.background = 'rgba(' + headerColor.r + ',' + headerColor.g + ',' + headerColor.b + ',' + 0 + ')' ;
	    	}
	    };

	    function headerColorOnScroll (color, scroll) {
	    	if (color) {
	        	if (scroll < 50) {
		        	element[0].style.background = 'rgba(' + color.r + ',' + color.g + ',' + color.b + ',' + 0 + ')' ;
	        	} else {
		        	element[0].style.background = 'rgba(' + color.r + ',' + color.g + ',' + color.b + ',' + 1 + ')' ;
	        	}
	    	}
	    }

	    function hexToRgb(hex) {
	        var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
	        return result ? {
	            r: parseInt(result[1], 16),
	            g: parseInt(result[2], 16),
	            b: parseInt(result[3], 16)
	        } : null;
	    }
	};
}]);