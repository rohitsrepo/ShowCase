angular.module('module.bucketmodal')
.factory('bucketmodalService', ['modalService', 'auth', function (modalService, auth) {
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

    var createBucketCallback = function () {
        return modalService.showModal({
            'templateUrl': '/static/js/components/bucketmodal/bucketmodal.create.tpl.html',
            'controller': 'bucketmodalCreateController',
        }).then(function (modal) {
            return modal.close;
        });
    };

    service.showCreateBucket = function () {
        return createBucketCallback();
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