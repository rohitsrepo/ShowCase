angular.module('InterpretApp')
.controller('interpretController', [
	'$scope',
	'analytics',
	'progress',
	'interpretationModel',
	'upload',
	'alert',
	'$http',
	function ($scope, analytics, progress, interpretationModel, upload, alert, $http) {

	var uploading;
	$scope.composition = {};

	$scope.init = function (id, url) {
		$scope.composition.id = id;
		$scope.composition.url = url;
		if (url) {
			analytics.logEvent('Composition', 'Init: ' + url);
		}
	};

	$scope.saveInterpretation = function () {
		analytics.logEvent('Composition', 'Add Interpretation', $scope.composition.url);

		progress.showProgress();

		if (!uploading){
			uploading = true;
			interpretationModel.addInterpretation($scope.composition.id, $('.new-interpretation').html())
			.then(function () {
				// Take to composition page
				progress.hideProgress();
				alert.showAlert("Your submission is under review.");
			}, function () {
				progress.hideProgress();
				alert.showAlert("This is not a valid submission.");
				uploading = false;
			});
		}
	};

	$scope.interpret = {};
	$scope.uploadFile = function (file) {
		progress.showProgress();
		return upload({
			url: '/compositions/' + $scope.composition.id + '/interpretation-images',
			method: 'POST',
			data: {'image': file}
		}).then(
			function (response) {
				progress.hideProgress();
				return response.data;
			},
			function (response) {
				progress.hideProgress();
				alert.showAlert('Error uploading file');
			}
		);
	};

	$scope.deleteFile = function (id) {
		return $http.delete('/compositions/' + $scope.composition.id + '/interpretation-images/'+id);
	};
}]);