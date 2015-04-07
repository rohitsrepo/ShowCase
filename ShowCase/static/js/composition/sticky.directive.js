angular.module("CompositionApp")
.directive('sticky', ["$document", "$window", function($document, $window) {
	return {
		restrict: 'A', 
		link: linkFn
	};

	var elem, topMark, absoluteLeft, relativeLeft, parentBottom, elementHeight, scrollTop, elemBottom, stickState;
	var offset = 100;
	var firstRun = true;

	function StickyHandler() {
		scrollTop = $document.scrollTop();
		elemBottom = scrollTop + elementHeight + offset;

		if(scrollTop > topMark - offset){
			if (elemBottom < parentBottom) {
				stickState = "sticky";
				Stick();
			} else {
				if(stickState == 'top')
				{
					return;
				}
				stickState = "fixToBottom";
				FixToBottom();
			}
		} else {
				stickState = "top";
				RemoveAllStyle();
		}
	};

	function Stick() {
		absoluteLeft = elem[0].getBoundingClientRect().left;

		if (elemBottom < parentBottom) {
			elem[0].style.cssText = "";
			elem
				.css('width',      elem[0].offsetWidth+'px')
				.css('position',   'fixed')
				.css('top',       offset+'px')
				.css('left',       absoluteLeft)
		}
	};

	function FixToBottom() {
		absoluteLeft = elem[0].getBoundingClientRect().left;
		relativeLeft = absoluteLeft - elem[0].parentElement.getBoundingClientRect().left;
		RemoveAllStyle();
		elem
			.css('position',   'absolute')
			.css('bottom',       '0px')
			.css('left',       relativeLeft)
	};

	function RemoveAllStyle() {
		elem[0].style.cssText = "";
	};

	function OnResize() {
		RemoveAllStyle();
		init();
		if (stickState === "sticky"){
			Stick();
		} else if (stickState == "fixToBottom") {
			FixToBottom();
		}
	};

	function init () {
		offset = 100;
		topMark = elem.offset().top;
		elementHeight = elem[0].scrollHeight;
		var parent = angular.element(elem[0].parentElement);
		parentBottom = parent.offset().top + parent[0].scrollHeight;
	};

	function linkFn($scope, $elem, $attrs) {
		var firstRun = true;
		$document.bind('scroll', function () {
			if (firstRun) {
				firstRun = false;
				return;
			}

			if (topMark == undefined){
				elem = $elem;
				offset = 100;
				topMark = $elem.offset().top;
				elementHeight = $elem[0].scrollHeight;
				var parent = angular.element($elem[0].parentElement);
				parentBottom = parent.offset().top + parent[0].scrollHeight;
			}

			StickyHandler();
		});
		angular.element($window).bind('resize', function () {
			OnResize();
		});
	}
}]);

