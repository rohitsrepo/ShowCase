angular.module('module.bookmark', ['module.model', 'module.util'])
.factory('bookService', ['$q', 'auth', 'userModel', 'progress', 'alert', function ($q, auth, userModel, progress, alert) {
	var service = {};

	service.bookmark = function (art) {
		return auth.runWithAuth(function () {
			progress.showProgress();
			return userModel.bookmark(art.id).then(function (response) {
				progress.hideProgress();
				return $q.when();
			}, function () {
				progress.hideProgress();
				alert.showAlert('Unable to complete your request');
				return $q.reject();
			});
		});
	};

	service.unmark = function (art) {
		return auth.runWithAuth(function () {
			progress.showProgress();
			return userModel.unmark(art.id).then(function (response) {
				progress.hideProgress();
				return $q.when();
			}, function () {
				progress.hideProgress();
				alert.showAlert('Unable to complete your request');
				return $q.reject();
			});
		});
	};

	return service;
}]);