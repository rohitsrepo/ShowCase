angular.module('module.model')
.factory('activityModel', ['$http', '$q', function ($http, $q) {
    var service = {};

    service.userActivities = function (user_id, next_token) {
        next_token = next_token || '';

        return $http.get('/users/'+user_id+'/activities?next_token='+next_token).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.newsActivities = function (user_id, next_token) {
        next_token = next_token || '';

        return $http.get('/users/'+user_id+'/news?next_token='+next_token).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.notificationActivities = function (next_token) {
        next_token = next_token || '';

        return $http.get('/users/notifications?next_token='+next_token).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.markSeen = function (activityIds) {
        return $http.put('/users/notifications', data={'activity_ids': activityIds}).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    service.enrichActivities = function (activities) {
        return $http.post('/users/notifications', data={'activities': activities}).then(function (response) {
            return response.data;
        }, function (response) {
            return $q.reject(response);
        });
    };

    return service;
}]);