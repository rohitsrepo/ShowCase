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
            console.log("updates")
            updateNsfw($scope.user.nsfw);
        }
        skipOnce = false;
    })

    $scope.uploadPicture = function (file) {
        progress.showProgress();
        upload({
            url: '/users/reset-picture',
            method: 'POST',
            data: {'picture': file}
        }).then(
            function (response) {
                progress.hideProgress();
                console.log(response);
                $scope.user.picture = response.data.picture
                // update the user image with response
            },
            function (response) {
                progress.hideProgress();
                alert.showAlert("Unable to update");
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