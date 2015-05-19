angular.module('UploadApp')
.controller('uploadController', ['$scope',
	'upload',
	'$window',
	'progress',
	'auth',
	function(
		$scope,
		upload,
		$window,
		progress,
		auth) {
	'use strict';

	function checkOrAddArtist () {
		if ($scope.art.artist === undefined || JSON.parse($scope.art.artist).id == -1){
			$scope.art.artist = JSON.stringify({'id': -1,'name': $('.artist-input')[0].value})
		}
	}

	$scope.art = {};

	$scope.uploadArt = function () {
    	progress.showProgress();
    	checkOrAddArtist();
		upload({
			url: '/compositions',
			method: 'POST',
			data: $scope.art
		}).then(
			function (response) {
				progress.hideProgress();
				$window.location.href="/arts/" + response.data.slug;
			},
			function (response) {
				progress.hideProgress();
			}
		);
	};

	$scope.selectArtist = function (selectedArtist) {
		if (selectedArtist === undefined){
			$scope.art.artist = JSON.stringify({'id': -1,'name': $('.artist-input')[0].val})
		} else {
			$scope.art.artist = selectedArtist.originalObject.id;
		}
	}
}]);