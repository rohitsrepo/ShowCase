angular.module('UserApp')
.controller('userProfileController', ['$scope', 'followService', 'usermodalService', 'alert', 'progress', function ($scope, followService, usermodalService, alert, progress) {
	$scope.hideName = true;
	$scope.artist = {'is_followed': false};

	$scope.init = function (id, is_followed, is_me) {
		$scope.artist.id = id;
        $scope.artist.is_followed = is_followed == 'True';
		$scope.artist.is_me = is_me == 'True';
	};

	$scope.handleFollow = function () {
        var artist = $scope.artist;

		if (artist.is_followed) {
			followService.unfollow(artist).then(function () {
                artist.is_followed = false;
            });
		} else {
			followService.follow(artist).then(function () {
                artist.is_followed = true;
            });
		}
	};

    $scope.showFollows = function () {
        usermodalService.showFollows($scope.artist);
    };

    $scope.showFollowers = function () {
        usermodalService.showFollowers($scope.artist).then(function (followStatus) {
            if (followStatus == 'followed') {
                $scope.artist.is_followed = true;
            }
        });
    };
}]);