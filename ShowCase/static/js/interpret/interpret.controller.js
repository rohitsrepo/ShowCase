angular.module('InterpretApp')
.controller('interpretController', [
	'$scope',
	'analytics',
	'progress',
	'interpretationModel',
	'confirmModalService',
	'upload',
	'alert',
	'$http',
	'$timeout',
	'$window',
	function ($scope, analytics, progress, interpretationModel, confirmModalService, upload, alert, $http, $timeout, $window) {

	var uploading;
	$scope.composition = {};
	$scope.hideName = true;
	$scope.interpret = {};
	$scope.composition = {};

	$scope.init = function (id, compositionSlug, title) {
		$scope.interpret.id = id;
		$scope.interpret.title = title;
		$scope.composition.slug = compositionSlug;
	};

	$scope.saveInterpretation = function () {
		// analytics.logEvent('Composition', 'Save Interpretation', $scope.composition.url);

		if (!uploading){
			progress.showProgress();
			uploading = true;

			var title = $scope.interpret.title ? $scope.interpret.title : 'Untitled';
			var interpretation = $('.new-interpretation').html() ? $('.new-interpretation').html(): '';

			console.log('title', title);
			console.log('interpretation', interpretation);

			interpretationModel.addInterpretation($scope.interpret.id, title, interpretation, true)
			.then(function (response) {
				progress.hideProgress();
				uploading = false;
				document.querySelector('.draft-text').className += ' show';

				$timeout(function () {
					document.querySelector('.draft-text').classList.remove("show");
				}, 2000);
			}, function () {
				progress.hideProgress();
				alert.showAlert("Unable to save data");
				uploading = false;
			});
		}
	};

	$scope.publishInterpretation = function () {
		// analytics.logEvent('Composition', 'Add Interpretation', $scope.composition.url);

		if (!uploading){
			progress.showProgress();
			uploading = true;
			interpretationModel.addInterpretation($scope.interpret.id, $scope.interpret.title, $('.new-interpretation').html(), false)
			.then(function (response) {
				// Take to composition page
				progress.hideProgress();
				window.location = response.url;
			}, function () {
				progress.hideProgress();
				alert.showAlert("Unable to save data");
				uploading = false;
			});
		}
	};

	$scope.deleteInterpretation = function (index) {
	    progress.hideProgress();

	    confirmModalService.showDeleteConfirm().then(function () {
	        interpretationModel.delete($scope.interpret.id).then(function () {
	            progress.hideProgress();
	            window.location.href = '/arts/' + $scope.composition.slug;
	        }, function () {
	            progress.hideProgress();
	            alert.showAlert('Currently unable to remove this draft');
	        });
	    });
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
		progress.showProgress();
		url = '/compositions/' + $scope.composition.id + '/interpretation-images';

		// Ideally this logic should exist in some service so that it can be shared, here we are using scope to share that data
		return $http.post(url, data={'source_type': 'CRP', 'box': cropBox}).then(function (response) {
			progress.hideProgress();
			return response.data;
		}, function () {
			progress.hideProgress();
			alert.showAlert("Error cropping the image");
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
}]).directive('fitImage', function () {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            element.bind('load', function () {
               imgElement = element[0]
               var imgClass = (imgElement.width/imgElement.height > 1) ? 'landscape' : 'potrait';
               element.addClass(imgClass);
            })
        }
    }
}).directive('saveDraft', function () {
	var debounce = function (fn, delay) {
	    var timer = null;

	    return function () {
	        var context = this, args = arguments;
	        clearTimeout(timer);
	        timer = setTimeout(function () {
	            fn.apply(context, args);
	        }, delay);
	    };
	};
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {

			var processor = debounce(function () {
				scope.saveInterpretation();
			}, 5000);
            element.bind('input', processor);
        }
    }
});