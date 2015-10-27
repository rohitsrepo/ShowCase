angular.module('UserSettingsApp')
.controller('userSettingsController', ['$scope',
    'userModel',
    'alert',
    'progress',
    'upload',
    function ($scope, userModel, alert, progress, upload) {

    $scope.hideName = true;

    var resetForm = function (form) {
        form.$setPristine();
        form.$setUntouched();
    };

    $scope.user = {};

    $scope.init = function (id, email, name, about, nsfw, picture) {
        $scope.user.id = id;
        $scope.user.email = email;
        $scope.user.name = name;
        $scope.user.about = about;
        $scope.user.nsfw = nsfw == 'True';
        $scope.user.picture = picture;
    };

    $scope.updateName = function (name, form) {
        progress.showProgress();

        userModel.resetName(name).then(function (response) {
            progress.hideProgress();
            $scope.user.name = response.name
            resetForm(form);
        }, function (response){
            progress.hideProgress();
            alert.showAlert("Unable to update");
        })
    };

    $scope.updateAbout = function (about, form) {
        progress.showProgress();

        userModel.resetAbout(about).then(function (response) {
            progress.hideProgress();
            $scope.user.about = response.about
            resetForm(form);
        }, function (response){
            progress.hideProgress();
            alert.showAlert("Unable to update");
        });
    };

    var updateNsfw = function (nsfw) {
        userModel.resetNsfw(nsfw).then(function (response) {
            progress.hideProgress();
        }, function (response){
            progress.hideProgress();
            alert.showAlert("Unable to update");
        });
    }

    var skipOnce = true;
    $scope.$watch(function () {
        return $scope.user.nsfw;
    }, function () {
        if (!skipOnce) {
            updateNsfw($scope.user.nsfw);
        }
        skipOnce = false;
    })

    userModel.getMailOptions().then(function (response) {
        $scope.mailOptions = response
    }, function (response){
        alert.showAlert("Unable to get mail options");
    });

    var updateMailOptions = function (mailOptions) {
        progress.showProgress();
        userModel.resetMailOptions(mailOptions).then(function (response) {
            progress.hideProgress();
        }, function (response){
            progress.hideProgress();
            alert.showAlert("Unable to update mail options");
        });
    }

    var skipOnceMail = true;
    $scope.$watch(function () {
        return $scope.mailOptions;
    }, function () {
        if (!skipOnceMail) {
            updateMailOptions($scope.mailOptions);
        }
        skipOnceMail = false;
    }, true)

    $scope.profilePicture = {};

    $scope.urlPictureUpload = function () {
        progress.showProgress();
        $scope.profilePicture.upload_type = 'url';

        userModel.resetPicture($scope.profilePicture).then(function () {
            progress.hideProgress();
            window.location.reload();
        } , function () {
            progress.hideProgress();
            alert.showAlert("Error fetching data for the image");
        })
    };

    $scope.uploadPicture = function (pictureFile) {
        progress.showProgress();

        $scope.profilePicture.upload_type = 'upl';
        $scope.profilePicture.upload_image = pictureFile;

        upload({
            url: '/users/reset-picture',
            method: 'POST',
            data: $scope.profilePicture
        }).then(
            function (response) {
                progress.hideProgress();
                window.location.reload();
            },
            function (response) {
                $scope.uploadingBackground = false;
                progress.hideProgress();
                alert.showAlert('Unable to upload image');
            }
        );
    };

}])
.directive('uploadPicture', [function () {
    return function (scope, element, attributes) {
        element.bind("change", function (changeEvent) {
            scope.uploadPicture(changeEvent.target.files[0]);
        });
    }
}]);