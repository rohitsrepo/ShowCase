angular.module("module.curtainLeft")
.directive('addCurtainLeft', ['curtainLeft', '$document', '$timeout', function (curtainLeft, $document, $timeout) {

	return {
		restrict: "A",
		link: function (scope, element, attrs) {
			var curtainElement, curtainModal;
			var isActive = false;
			var curtainOverlay = angular.element(document.getElementsByClassName("curtain-overlay-placeholder"));

			var removeCurtain = function () {
	            curtainElement.removeClass('animated fadeInLeft');
	            curtainElement.addClass('animated fadeOutLeft');
	            curtainElement.animate({marginLeft:-500}, 300);
	            curtainOverlay.removeClass("curtain-overlay");
	            $timeout(function () {curtainModal.close()}, 300);
	            $document.unbind("click");
	            isActive = false;
			}

			var addCurtain = function () {
	            curtainElement.removeClass('animated fadeOutLeft');
	            curtainElement.addClass('animated fadeInLeft');
	            curtainElement.animate({marginLeft:0}, 400);

	            $timeout(function () {
	            	curtainOverlay.addClass("curtain-overlay")
	            }, 250);

	            $document.bind("click", function (event) {
					var isClickedInside = curtainElement.find(event.target).length > 0 || curtainElement[0] == event.target;
					if (!isClickedInside) {
						removeCurtain();
					}
				});

				isActive = true;
			};

			var options = {
				templateUrl: "/static/js/components/curtain-left/curtain-left.tpl.html",
				controller: "leftCurtainController",
				appendElement: element.parent()
			};

			element.bind("click", function (event) {
				console.log(curtainElement);
				if (!isActive){
				var left_curtain = curtainLeft.getCurtain(options);
					left_curtain.then(function(result){
						curtainModal = result;
						curtainElement = curtainModal.element;
						addCurtain();
					});
				} else {
					removeCurtain();
				}
			});
		}
	};
}]);