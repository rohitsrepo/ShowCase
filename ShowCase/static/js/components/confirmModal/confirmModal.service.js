angular.module('module.confirmModal')
.factory('confirmModalService', ['$q', 'modalService', 'auth', function ($q, modalService, auth) {
    var service = {};

    service.showDeleteConfirm = function () {
        var deferred = $q.defer();
        var data = {'message': 'Are you sure you want to delete this item?'};

        modalService.showModal({
            'templateUrl': '/static/js/components/confirmModal/confirmModal.tpl.html',
            'controller': 'confirmModalController',
            'inputs' : {'data': data}
        }).then(function (modal) {
            modal.close.then(function(result) {
                if (result == 'confirm'){
                    deferred.resolve(result);
                } else {
                    deferred.reject(result);
                }
            }, function(result) {
                deferred.reject(result);
            });
        });

        return deferred.promise;
    };

    return service;
}]);