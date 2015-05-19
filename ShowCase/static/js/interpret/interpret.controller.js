angular.module('InterpretApp')
.controller('interpretController', [
	'$scope',
	'analytics',
	'progress',
	'interpretationModel',
	function ($scope, analytics, progress, interpretationModel) {

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
		console.log("start uploading");
		analytics.logEvent('Composition', 'Add Interpretation', $scope.composition.url);

		progress.showProgress();

		if (!uploading){
			uploading = true;
			interpretationModel.addInterpretation($scope.composition.id, $('.new-interpretation').html())
			.then(function () {
				// Take to composition page
		console.log("start suc");
				// showAlert("Your submission is under review.");
			}, function () {
				progress.hideProgress();
		console.log("start fail");
				// showAlert("This is not a valid submission.");
				uploading = false;
			});
		}
	};

	$scope.interpret = {};
	$scope.uploadFile = function (ufile) {
		console.log("Will be uploading file: ", ufile);
	};
}]);