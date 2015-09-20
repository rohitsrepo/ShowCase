angular.module('module.followBucket', ['module.model', 'module.util'])
.factory('followBucketService', ['$q', 'auth',  'bucketModel', 'progress', 'alert', function ($q, auth, bucketModel, progress, alert) {
    var service = {};

    service.watchBucket = function (bucketId) {
        var deferred = $q.defer();

        auth.runWithAuth(function () {
            progress.showProgress();

            bucketModel.watch(bucketId).then(function (response) {
                progress.hideProgress();
                deferred.resolve();
            }, function () {
                progress.hideProgress();
                alert.showAlert("Currently unable to follow this series");
                deferred.reject();
            });
        });

        return deferred.promise;
    };

    service.unwatchBucket = function (bucketId) {
        var deferred = $q.defer();

        auth.runWithAuth(function () {
            progress.showProgress();

            bucketModel.unwatch(bucketId).then(function (response) {
                progress.hideProgress();
                deferred.resolve();
            }, function () {
                progress.hideProgress();
                alert.showAlert("Currently unable to un-follow this series");
                deferred.reject();
            });
        });

        return deferred.promise;
    };

    return service;
}]);