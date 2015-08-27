angular.module('module.util')
.directive('alertSupport', [ 'alert', function (alert) {
	return {
		restrict: 'E',
		replace: true,
		scope: {},
		template: '<section class="alerts" ng-cloak ng-show="alertMeta.show"><h4>[[alertMeta.content]]</h4></section>',
		link: function (scope, element, attrs) {
			scope.$watch(function () {
				return alert.show;
			}, function () {
				scope.alertMeta = {'content': alert.content, 'show': alert.show};
			}, true);

		}
	};
}]);