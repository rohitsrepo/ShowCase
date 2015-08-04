angular.module('UserApp')
.controller('userProfileController', ['$scope', 'userModel', 'alert', 'progress', function ($scope, userModel, alert, progress) {
	$scope.hideName = true;
	$scope.artist = {};

	$scope.init = function (id) {
		$scope.artist.id = id;
	};

	$scope.follow = function () {
		progress.showProgress();
		userModel.follow($scope.artist.id).then(function (response) {
			$scope.unfollowedNow = true;
			$scope.followedNow = false;
			progress.hideProgress();
		}, function () {
			progress.hideProgress();
			alert.showAlert('We are unable to process your response');
		});
	};

	$scope.unfollow = function () {
		progress.showProgress();
		userModel.unfollow($scope.artist.id).then(function (response) {
			$scope.followedNow = true;
			$scope.unfollowedNow = false;
			progress.hideProgress();
		}, function () {
			progress.hideProgress();
			alert.showAlert('We are unable to process your response');
		});
	};
}]);