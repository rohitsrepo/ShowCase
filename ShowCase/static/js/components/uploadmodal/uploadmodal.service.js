angular.module('module.uploadmodal')
.factory('uploadmodalService', ['modalService', 'auth', function (modalService, auth) {
    var service = {};

    service.showUpload = function (user) {
        modalService.showModal({
            'templateUrl': '/static/js/components/uploadmodal/uploadmodal.tpl.html',
            'controller': 'uploadmodalController',
            'inputs': {'user': user}
        })
    };

    return service;
}]);