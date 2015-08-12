angular.module('module.seriesmodal')
.factory('seriesmodalService', ['modalService', function (modalService) {
    var service = {};

    service.showSerieses = function (art) {
        return modalService.showModal({
            'templateUrl': '/static/js/components/seriesmodal/seriesmodal.tpl.html',
            'controller': 'seriesmodalController',
            'inputs' : {'art': art}
        }).then(function (modal) {
            return modal.close;
        });
    };

    return service;
}]);