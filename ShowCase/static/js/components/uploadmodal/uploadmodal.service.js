angular.module('module.uploadmodal')
.factory('uploadmodalService', ['modalService', 'auth', function (modalService, auth) {
    var service = {};

    service.showUpload = function (art) {
        modalService.showModal({
            'templateUrl': '/static/js/components/uploadmodal/uploadmodal.tpl.html',
            'controller': 'uploadmodalController'
        })
    };

    return service;
}]);