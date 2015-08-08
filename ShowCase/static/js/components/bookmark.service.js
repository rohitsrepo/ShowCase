angular.module('module.bookmark', ['module.model', 'module.util'])
.factory('bookService', ['$q', 'userModel', 'progress', 'alert', function ($q, userModel, progress, alert) {
	var service = {};

	service.bookmark = function (art) {
		progress.showProgress();
		return userModel.bookmark(art.id).then(function (response) {
			progress.hideProgress();
			return $q.when();
		}, function () {
			progress.hideProgress();
			alert.showAlert('We are unable to process your response');
			return $q.reject();
		});
	};

	service.unmark = function (art) {
		progress.showProgress();
		return userModel.unmark(art.id).then(function (response) {
			progress.hideProgress();
			return $q.when();
		}, function () {
			progress.hideProgress();
			alert.showAlert('We are unable to process your response');
			return $q.reject();
		});
	};

	return service;
}]);