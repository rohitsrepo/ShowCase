angular.module("module.model")
.factory('bucketModel', ['$http', '$log', '$q', function ($http, $log, $q) {
    "use strict";

    var service = {};

    service.artBuckets = function (compositionId) {
        return $http.get('/compositions/' + compositionId + '/buckets').then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.userBuckets = function (userId, artId) {
        return $http.get('/users/' + userId + '/buckets?composition=' + artId).then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.addToBucket = function (bucketId, compositionId, description) {
        return $http.put('/buckets/' + bucketId + '/arts',
            {'composition_id': compositionId, 'description': description})
        .then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.removeFromBucket = function (bucketId, compositionId) {
        return $http.delete('/buckets/' + bucketId + '/arts/' + compositionId).then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.create = function (bucket) {
        return $http.post('/buckets', bucket).then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.bucketArts = function (bucketId) {
        return $http.get('/buckets/' + bucketId + '/arts').then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.getBucket = function (bucketSlug) {
        return $http.get('/buckets/' + bucketSlug).then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.editBucket = function (bucket) {
        return $http.put('/buckets/' + bucket.slug, bucket).then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.deleteBucket = function (bucketSlug) {
        return $http.delete('/buckets/' + bucketSlug).then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.updateBackground = function (bucketId, bucket_background) {
        return $http.post('/buckets/' + bucketId + '/background', bucket_background).then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.watch = function (bucketId) {
        return $http.put('/buckets/' + bucketId + '/watchers').then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.unwatch = function (bucketId) {
        return $http.delete('/buckets/' + bucketId + '/watchers').then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    return service;
}]);