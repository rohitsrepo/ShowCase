var reader = angular.module('reader.module', [
    'security.service',
    'artifact.composition',
    'helper.logger',
    'angularFileUpload',
    'ui.router',
    'artifact.bookmark'
]);

reader.controller('readerController', [
    '$scope',
    'securityFactory',
    'compositionFactory',
    'logger',
    '$upload',
    '$state',
    '$log',
    'bookmarkFactory',
    '$window',
    function ($scope, securityFactory, compositionFactory, logger, $upload, $state, $log, bookmarkFactory, $window) {
        'use strict';
    
        var file;

        $scope.compositions = compositionFactory.manager.query();
        $scope.newComposition = {};

        $scope.voting = function (index, vote) {
            compositionFactory.votes.put($scope.compositions[index].id, vote).then(function (res) {
                if (res) {
                    $scope.compositions[index].vote = res.data;
                    $scope.compositions[index].IsVoted = true;
                }
            }, function (res) {
                //TODO handle error according to status of error.
                // Global exception handling.
                logger('Reader controller...error while putting votes', res);
                if (res.status === 403) {
                    alert('Seems like you have already voted mate!!!');
                }
            });
        };

        $scope.onFileSelect = function ($files) {
            file = $files;
        };

        $scope.submitComposition = function () {
            file = file[0];
            $scope.upload = $upload.upload({
                url: 'compositions', //upload.php script, node.js route, or servlet url
                method: 'POST',
                //withCredentials: true,
                data: $scope.newComposition,
                file: file,
                fileFormDataName: "matter"
            }).progress(function (evt) {
                $log.info('percent: ' + parseInt(100.0 * evt.loaded / evt.total));
            }).success(function (data, status, headers, config) {
                // file is uploaded successfully
                //TODO - update this logic - page upload should not be required.
                $window.location.href = $state.href('composition', {compositionId: data.id, slug: data.slug});
                $window.location.reload();
            });
        };
        
        $scope.bookmark = function (compositionId, index) {
        if (securityFactory.checkForAuth()) {
            bookmarkFactory.addBookmark($scope.currentUser.id, compositionId).then(function (res) {
                if (res) {
                    $scope.compositions[index].IsBookmarked = true;
                } else {
                    $log.info('Seems like auth reluctance by user.');
                }
            }, function (res) {});
        }
    };
    }]);