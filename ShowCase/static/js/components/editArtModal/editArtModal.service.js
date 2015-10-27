angular.module('module.editArtModal')
.factory('editArtModalService', ['modalService', 'auth', function (modalService, auth) {
    var service = {};

    service.showEditArt = function (art) {
    	auth.runWithAuth(function (user) {
    		if (user) {
	    		modalService.showModal({
	    		    'templateUrl': '/static/js/components/editArtModal/editArtModal.tpl.html',
	    		    'controller': 'editArtModalController',
                    'inputs': {
                        'art': art
                    }
	    		});
    		}
    	});

    };

    return service;
}]);