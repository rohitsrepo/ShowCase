angular.module("module.model")
.factory('compositionModel', ['$http', '$log', '$q', function ($http, $log, $q) {
	"use strict";

	var base_url = "/compositions";
	var service = {};

	service.getExplores = function (pageVal) {
		var url = base_url + "/explore" + "?page=" + pageVal;
		return $http.get(url).then(function (response) {
			return response.data;
		},function (response) {
			$log.error("Error fetching art list.", response);
		});
	};

    service.getBookMarkers = function (compositionId) {
        return $http.get('/compositions/' + compositionId + '/bookmarkers').then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.urlImageUploader = function (art) {
        return $http.post('/compositions/matter', art).then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.addArt = function (art) {
        return $http.post('/compositions', art).then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.getArt = function (artSlug) {
        return $http.get('/compositions/' + artSlug).then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.updateArt = function (artSlug, data) {
        return $http.put('/compositions/' + artSlug, data).then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.deleteArt = function (artSlug) {
        return $http.delete('/compositions/' + artSlug).then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

    service.getAssociates = function (artId) {
        return $http.get('/compositions/' + artId + '/associates').then(function (response) {
            return response.data;
        }, function (error) {
            return $q.reject(error);
        });
    };

	return service;
}]);