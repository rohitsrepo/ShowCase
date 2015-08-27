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

    return service;
}]);