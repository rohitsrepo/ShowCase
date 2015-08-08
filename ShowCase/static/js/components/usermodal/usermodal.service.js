angular.module('module.usermodal')
.factory('usermodalService', ['modalService', function (modalService) {
    var service = {};

    var showuserModal = function (target, modalType) {
        return modalService.showModal({
            'templateUrl': '/static/js/components/usermodal/usermodal.tpl.html',
            'controller': 'usermodalController',
            'inputs' : {
                'target': target,
                'modalType': modalType
            }
        }).then(function (modal) {
            return modal.close;
        });
    };

    service.showBookMarkers = function (art) {
        return showuserModal(art, 'bookmarkers');
    };

    service.showFollowers = function (user) {
        return showuserModal(user, 'followers');
    };

    service.showFollows = function (user) {
        return showuserModal(user, 'follows');
    };

    return service;
}]);