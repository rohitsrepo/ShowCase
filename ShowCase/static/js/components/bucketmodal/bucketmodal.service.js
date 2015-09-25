angular.module('module.bucketmodal')
.factory('bucketmodalService', ['$q', 'modalService', 'auth', function ($q, modalService, auth) {
    var service = {};

    service.showArtBuckets = function (art) {
        modalService.showModal({
            'templateUrl': '/static/js/components/bucketmodal/bucketmodal.show.tpl.html',
            'controller': 'bucketmodalShowController',
            'inputs' : {'art': art}
        })
    };

    var addToBucketCallback = function (art) {
        auth.getCurrentUser().then(function (user) {
            modalService.showModal({
                'templateUrl': '/static/js/components/bucketmodal/bucketmodal.add.tpl.html',
                'controller': 'bucketmodalAddController',
                'inputs' : {
                    'art': art,
                    'user': user
                }
            });
        });
    };

    service.showAddToBucket = function (art) {
        auth.runWithAuth(addToBucketCallback(art));
    };

    service.showCreateBucket = function () {
        var deferred = $q.defer();

        auth.runWithAuth(function () {
            modalService.showModal({
                'templateUrl': '/static/js/components/bucketmodal/bucketmodal.create.tpl.html',
                'controller': 'bucketmodalCreateController',
            }).then(function (modal) {
                modal.close.then(function(result) {
                    deferred.resolve(result);
                }, function(result) {
                    deferred.reject(result);
                });
            });
        });

        return deferred.promise;
    };

    service.showEditBucket = function (bucket) {
        var deferred = $q.defer();

        auth.runWithAuth(function () {
            modalService.showModal({
                'templateUrl': '/static/js/components/bucketmodal/bucketmodal.edit.tpl.html',
                'controller': 'bucketmodalEditController',
                inputs: {'bucket': bucket}
            }).then(function (modal) {
                modal.close.then(function(result) {
                    if (result && result.edited) {
                        deferred.resolve(result.bucket);
                    } else {
                        deferred.reject(result);
                    }
                }, function(result) {
                    deferred.reject(result);
                });
            });
        });

        return deferred.promise;
    };

    service.showBucketArts = function (bucket) {
        modalService.showModal({
            'templateUrl': '/static/js/components/bucketmodal/bucketmodal.content.tpl.html',
            'controller': 'bucketmodalContentController',
            'inputs' : {'bucket': bucket}
        })
    };

    return service;
}]);