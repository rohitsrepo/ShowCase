angular.module('module.admiration', ['module.model', 'module.util'])
.factory('admireService', ['$q', 'auth', 'admirationModel', 'progress', 'alert', function ($q, auth, admirationModel, progress, alert) {
	var service = {};

	var admire = function (object_id, content_type) {
		return auth.runWithAuth(function () {
			progress.showProgress();
			return admirationModel.admire(object_id, content_type).then(function (response) {
				progress.hideProgress();
				return $q.when();
			}, function () {
				progress.hideProgress();
				alert.showAlert('Unable to complete your request');
				return $q.reject();
			});
		});
	};

    service.admireArt = function (art) {
        return admire(art.id, admirationModel.TypeArt);
    };

    service.admireBucket = function (bucket) {
        return admire(bucket.id, admirationModel.TypeBucket);
    };

	var unadmire = function (object_id, content_type) {
		return auth.runWithAuth(function () {
			progress.showProgress();
			return admirationModel.unadmire(object_id, content_type).then(function (response) {
				progress.hideProgress();
				return $q.when();
			}, function () {
				progress.hideProgress();
				alert.showAlert('Unable to complete your request');
				return $q.reject();
			});
		});
	};

    service.unadmireArt = function (art) {
        return unadmire(art.id, admirationModel.TypeArt);
    };

    service.unadmireBucket = function (bucket) {
        return unadmire(bucket.id, admirationModel.TypeBucket);
    };

	return service;
}]);