angular.module('module.interpret', ['ngMaterial', "module.model"])
.factory('interpretation', ['$mdDialog', function ($mdDialog) {
	var service = {};

	service.add = function (event, compositionId) {
		return $mdDialog.show({
			targetEvent: event,
            templateUrl: '/static/js/components/interpret/interpret.tpl.html',
            controller: 'interpretController',
            disableParentScroll: false,
            locals: {
            	'compositionId': compositionId
            }
		});
	};

	return service;
}]);