angular.module("module.topbar", ["module.auth"])
.directive("topbar", [function () {
	return {
		restrict: 'E',
		replace: true,
		templateUrl: "/static/js/components/topbar/topbar.tpl.html"
	};
}]);