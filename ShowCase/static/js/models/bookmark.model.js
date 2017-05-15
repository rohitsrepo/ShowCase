angular.module("module.model")
.factory('bookmarkModel', ['$http', '$q', function ($http, $q) {
    "use strict";

    var service = {};

    service.TypeBucket = 'BK';
    service.TypeArt = 'AR';
    service.TypeInterpret = 'IN';

    service.bookmark = function (object_id, content_type) {
        return $http.post('/bookmarks',
            {'content_type': content_type,
            'object_id': object_id})
        .then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.unmark = function (object_id, content_type) {
        return $http({'url': '/bookmarks',
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

    service.getBookMarks = function (user_id, page) {
        return $http.get('/bookmarks?page='+page).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    return service;
}]);