angular.module('UploadApp')
.controller('uploadController', ['$scope',
	'$cookies',
	'FileUploader',
	'$window',
	'progress',
	function(
		$scope,
		$cookies,
		FileUploader,
		$window,
		progress) {
	'use strict';

	$scope.art = {};

	var uploader = $scope.uploader = new FileUploader({
	            url: '/compositions',
	            alias: 'matter',
	            headers: {'X-CSRFToken': $cookies.csrftoken},
	            queueLimit: 1
	        });

		uploader.formData.push($scope.art);

	        // FILTERS

	        uploader.filters.push({
	            name: 'imageFilter',
	            fn: function(item, options) {
	                var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
	                return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
	            }
	        });

	        uploader.onSuccessItem = function(fileItem, response, status, headers) {
	        	progress.hideProgress();
				$window.location.href="/arts/" + response.slug;
	        };

	        $scope.uploadArt = function () {
	        	progress.showProgress();
	        	$scope.showUploading = true;
	        	uploader.formData.push($scope.art);
	        	uploader.queue[0].upload();
	        }
	
}]);