angular.module("module.curtainRight")
.directive('addCurtainRight', ['curtainRight', '$document', '$timeout', function (curtainRight, $document, $timeout) {

	return {
		restrict: "A",
		link: function (scope, element, attrs) {
			var curtainElement;
			var curtainOverlay = angular.element(document.getElementsByClassName("curtain-overlay-placeholder"));

			var removeCurtain = function () {
	            curtainElement.removeClass('animated fadeInRight');
	            curtainElement.animate({marginRight:-500}, 300);
            	curtainOverlay.removeClass("curtain-overlay");
	            element.removeClass("animated fadeOutLeft");
	            element.addClass("animated fadeInRight");
	            element.show();
			}

			var addCurtain = function () {
				curtainElement.removeClass("animated animated fadeOutRight");
				curtainElement.addClass("animated fadeInRight");
				curtainElement.animate({marginRight:0}, 400);
	            element.removeClass("animated fadeInRight");
	            element.addClass("animated fadeOutLeft");
	            $timeout(function () {
	            	element.hide();
	            }, 500);
	            $timeout(function () {
	            	curtainOverlay.addClass("curtain-overlay");
	            }, 250);

	            $document.bind("click", function (event) {
					var isClickedInside = curtainElement.find(event.target).length > 0 || curtainElement[0] == event.target;
					if (!isClickedInside) {
						removeCurtain();
					}
				});
			};

			var options = {
				templateUrl: "/static/js/components/curtain-right/curtain-right.tpl.html",
				controller: "rightCurtainController",
				appendElement: element.parent()
			};

			element.bind("click", function (event) {
				var right_curtain = curtainRight.getCurtain(options);
				right_curtain.then(function(curtainModal){
					curtainElement = curtainModal.element;
					addCurtain();
				});
			});
		}
	};
}]);