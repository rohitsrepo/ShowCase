angular.module('module.util', [])
.directive('headerScroll', ['$window', '$interval', function ($window, $interval) {
	return function(scope, element, attrs) {
	    var didScroll;
	    var lastScrollTop = 0;
	    var delta = 3;
	    var navbarHeight = element.outerHeight();
	    var headerColor;
	    var hasCrossedThreshhold = false;

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

	        if (st> navbarHeight && !hasCrossedThreshhold) {
	        	hasCrossedThreshhold = true;
	        	element.addClass('header-fix');
	        } else if (st == 0) {
	        	element.removeClass('header-fix');
	        	hasCrossedThreshhold = false;
	        }

	        // Make sure they scroll more than delta
	        

	        // If they scrolled down and are past the navbar, add class .nav-up.
	        // This is necessary so you never see what is "behind" the navbar.
	        if (st > lastScrollTop && st > navbarHeight){
	        	if(Math.abs(lastScrollTop - st) <= delta)
	        	    return;
	            // Scroll Down
	            element.removeClass('header-pull-down');
	        } else {
	            // Scroll Up
	            if(st + $(window).height() < $(document).height()) {
	                element.addClass('header-pull-down');
	            }
	        }

	        lastScrollTop = st;
	    }

	    function headerColorInit () {
	    	if (scope.headerColor){
	    		headerColor = hexToRgb(scope.headerColor);
	    		element[0].style.background = 'rgba(' + headerColor.r + ',' + headerColor.g + ',' + headerColor.b + ',' + 0 + ')' ;
	    		element.addClass('white');
	    	}
	    };

	    function headerColorOnScroll (color, scroll) {
	    	if (color) {
	        	if (scroll < 50) {
		        	element[0].style.background = 'rgba(' + color.r + ',' + color.g + ',' + color.b + ',' + 0 + ')';
		        	element.addClass('white');
	        	} else {
		        	element[0].style.background = 'rgba(' + color.r + ',' + color.g + ',' + color.b + ',' + 1 + ')';
		        	if (scope.headerTextColor != 'white') {
		        		element.removeClass('white');
		        	}
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