angular.module('module.admiration', ['module.model', 'module.util'])
.factory('admireService', ['$q', 'auth', 'admirationModel', 'progress', 'alert', function ($q, auth, admirationModel, progress, alert) {
	var service = {};

    service.admirationOptions = ['',
        'Beautiful',
        'Unusual',
        'Thought-Provoking',
        'Repulsive',
        'Soothing',
        'Saddening',
        'Dark',
        'Touching',
        'Entertaining',
        'Interesting',
        'Inspiring'
    ]

	var admire = function (object_id, content_type, option) {
		return auth.runWithAuth(function () {
			progress.showProgress();
			return admirationModel.admire(object_id, content_type, option).then(function (response) {
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
        return admire(art.id, admirationModel.TypeArt, '');
    };

    service.admireBucket = function (bucket, option) {
        return admire(bucket.id, admirationModel.TypeBucket, option);
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

    var getAdmirationOptions = function (object_id, content_type) {
        progress.showProgress();
        return admirationModel.getAdmirationOptions(object_id, content_type).then(function (response) {
            progress.hideProgress();
            return $q.when(response);
        }, function () {
            progress.hideProgress();
            alert.showAlert('Unable to complete your request');
            return $q.reject();
        });
    };

    service.getAdmirationOptionsArt = function (art) {
        return getAdmirationOptions(art.id, admirationModel.TypeArt);
    };

    service.getAdmirationOptionsBucket = function (bucket) {
        return getAdmirationOptions(bucket.id, admirationModel.TypeBucket);
    };

	return service;
}]);