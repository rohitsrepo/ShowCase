angular.module('module.collectionmodal')
.factory('collectionmodalService', ['modalService', function (modalService) {
    var service = {};

    service.showCollections = function (art) {
        return modalService.showModal({
            'templateUrl': '/static/js/components/collectionmodal/collectionmodal.tpl.html',
            'controller': 'collectionmodalController',
            'inputs' : {'art': art}
        }).then(function (modal) {
            return modal.close;
        });
    };

    return service;
}]);