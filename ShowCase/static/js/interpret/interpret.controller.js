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

	$scope.cropFile = function (cropBox) {
		url = '/compositions/' + $scope.composition.id + '/interpretation-images';

		// Ideally this logic should exist in some service so that it can be shared, here we are using scope to share that data
		return $http.post(url, data={'source_type': 'CRP', 'box': cropBox}).then(function (response) {
			return response.data;
		});
	};

	$scope.deleteFile = function (id) {
		return $http.delete('/compositions/' + $scope.composition.id + '/interpretation-images/'+id);
	};
}])
.directive("crop", ['alert', function (alert) {

	return {
		restrict: 'A',
		link: function (scope, element, attrs) {
			var showAlertCheck = true;
			scope.showCropper = function (callback) {
				if(showAlertCheck){
					scope.$apply(function () {
						alert.showAlert("Select part of image to crop");
					});
					showAlertCheck = false;
				}
				var cropper = element.imgAreaSelect({
					'imageHeight': element[0].naturalHeight,
					'imageWidth': element[0].naturalWidth,
					'onSelectEnd': handleSelection(callback)
				});
			};

			var handleSelection = function (callback) {
				return function (img, selection) {
					scope.hideCropper();
					callback(img, selection);
				};
			};

			scope.hideCropper = function () {
				var selector = element.imgAreaSelect({instance: true });
				selector.cancelSelection();
				selector.setOptions({'disable': true});
			}
		}
	};
}]);