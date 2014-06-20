var testCtrlModule = angular.module('controller.test', ['angularFileUpload']);

testCtrlModule.controller('testCtrl', ['$scope', '$upload', function ($scope, $upload) {
    $scope.composition = {type: "IM"};
   $scope.onFileSelect = function($files) {
    //$files: an array of files selected, each file has name, size, and type.
    for (var i = 0; i < $files.length; i++) {
      var file = $files[i];
      $scope.upload = $upload.upload({
        url: 'compositions', //upload.php script, node.js route, or servlet url
        method: 'POST',
        // headers: {'header-key': 'header-value'},
        // withCredentials: true,
        data: $scope.composition,
        file: file, // or list of files: $files for html5 only
        /* set the file formData name ('Content-Desposition'). Default is 'file' */
        fileFormDataName: "matter", //or a list of names for multiple files (html5).
        /* customize how data is added to formData. See #40#issuecomment-28612000 for sample code */
        //formDataAppender: function(formData, key, val){}
      }).progress(function(evt) {
        console.log('percent: ' + parseInt(100.0 * evt.loaded / evt.total));
      }).success(function(data, status, headers, config) {
        // file is uploaded successfully
        console.log(data);
      });
    }
  };
    
}]);