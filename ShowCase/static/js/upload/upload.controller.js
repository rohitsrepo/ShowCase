angular.module('UploadApp')
.controller('uploadController', ['$scope',
	'upload',
	'$window',
	'progress',
	function(
		$scope,
		upload,
		$window,
		progress) {
	'use strict';

	$scope.uploadArt = function () {
    	progress.showProgress();
		upload({
			url: '/compositions',
			method: 'POST',
			data: $scope.art
		}).then(
			function (response) {
				progress.hideProgress();
				$window.location.href="/arts/" + response.slug;
			},
			function (response) {
				progress.hideProgress();
			}
		);
	};	
}]);