angular.module('module.uploadmodal')
.factory('uploadmodalService', ['modalService', 'auth', function (modalService, auth) {
    var service = {};

    service.showUpload = function () {
    	auth.runWithAuth(function (user) {
    		if (user) {
	    		modalService.showModal({
	    		    'templateUrl': '/static/js/components/uploadmodal/uploadmodal.tpl.html',
	    		    'controller': 'uploadmodalController',
	    		});
    		}
    	});

    };

    return service;
}]);