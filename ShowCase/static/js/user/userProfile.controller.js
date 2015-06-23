angular.module('UserApp')
.controller('userProfileController', ['$scope', 'userModel', function ($scope, userModel) {
	$scope.hideName = true;
	$scope.artist = {};

	$scope.init = function (id) {
		$scope.artist.id = id;
	};

}]);