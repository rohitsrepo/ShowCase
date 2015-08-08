angular.module('UserApp')
.controller('userProfileController', ['$scope', 'userModel', 'alert', 'progress', function ($scope, userModel, alert, progress) {
	$scope.hideName = true;
	$scope.artist = {'is_followed': false};

	$scope.init = function (id, is_followed) {
		$scope.artist.id = id;
		$scope.artist.is_followed = is_followed == 'True';
	};

	var follow = function () {
		progress.showProgress();
		userModel.follow($scope.artist.id).then(function (response) {
			$scope.artist.is_followed = true;
			progress.hideProgress();
		}, function () {
			progress.hideProgress();
			alert.showAlert('We are unable to process your response');
		});
	};

	var unfollow = function () {
		progress.showProgress();
		userModel.unfollow($scope.artist.id).then(function (response) {
			$scope.artist.is_followed = false;
			progress.hideProgress();
		}, function () {
			progress.hideProgress();
			alert.showAlert('We are unable to process your response');
		});
	};

	$scope.handleFollow = function () {
		if ($scope.artist.is_followed) {
			unfollow();
		} else {
			follow();
		}
	};
}]);