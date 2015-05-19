angular.module('module.alert')
.directive('alertSupport', [ 'alert', function (alert) {
	return {
		restrict: 'E',
		replace: true,
		scope: {},
		template: '<section class="alerts" ng-cloak ng-show="alertMeta.show"><h4>[[alertMeta.content]]</h4></section>',
		link: function (scope, element, attrs) {
			scope.alertMeta = alert.meta;
		}
	};
}]);