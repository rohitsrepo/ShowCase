angular.module('module.bookmark')
.factory('bookService', ['$q', 'modalService', 'userModel', 'progress', 'alert', function ($q, modalService, userModel, progress, alert) {
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

	service.showBookMarkers = function (art) {
		return modalService.showModal({
            'templateUrl': '/static/js/components/bookmark/bookmark.tpl.html',
            'controller': 'bookmarkController',
            'inputs' : {'composition': art}
        }).then(function (modal) {
        	return modal.close;
        });
	};

	return service;
}]);