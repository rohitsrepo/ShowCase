angular.module("module.model")
.factory('bookmarkModel', ['$http', '$q', function ($http, $q) {
    "use strict";

    var service = {};

    service.TypeBucket = 'BK';
    service.TypeArt = 'AR';

    service.bookmark = function (object_id, bookmark_type) {
        return $http.post('/bookmarks',
            {'bookmark_type': bookmark_type,
            'object_id': object_id})
        .then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.unmark = function (object_id, bookmark_type) {
        return $http({'url': '/bookmarks',
            'method': 'DELETE',
            'data': {'bookmark_type': bookmark_type,
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