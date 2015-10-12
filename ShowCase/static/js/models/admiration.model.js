angular.module("module.model")
.factory('admirationModel', ['$http', '$q', function ($http, $q) {
    "use strict";

    var service = {};

    service.TypeBucket = 'BK';
    service.TypeArt = 'AR';

    service.admire = function (object_id, content_type) {
        return $http.post('/admirations',
            {'content_type': content_type,
            'object_id': object_id})
        .then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.unadmire = function (object_id, content_type) {
        return $http({'url': '/admirations',
            'method': 'DELETE',
            'data': {'content_type': content_type,
            'object_id': object_id},
            'headers': {"Content-Type": "application/json;charset=utf-8"}})
        .then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.getUserAdmirations = function (user_id, page) {
        return $http.get('/admirations/' + user_id + '?page='+page).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.getAdmirations = function (object_id, content_type) {
        return $http.get('/admirations?object_id='+object_id+'&content_type='+content_type).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    return service;
}]);