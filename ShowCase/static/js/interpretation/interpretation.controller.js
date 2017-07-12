angular.module("InterpretationApp")
.controller('interpretationController', [
    '$scope',
    'interpretationModel',
    'followService',
    'bookService',
    'confirmModalService',
    'shareModalService',
    'admireService',
    'progress',
    function($scope, 
        interpretationModel,
        followService, 
        bookService,
        confirmModalService,
        shareModalService,
        admireService,
        progress) {
    $scope.hideName = true;
    $scope.interpretation = {};

    var getInterpretAssociates = function () {
        interpretationModel.getRelated($scope.interpretation.id).then(function (response) {
            $scope.relatedBuckets = response.relatedBuckets;
            $scope.relatedInterprets = response.relatedInterprets;
            $scope.relatedWorks = response.relatedWorks;
            $scope.relatedCounts = response.counts;
        });
    };

    $scope.init = function (id, 
        title,
        text,
        is_admired, 
        is_bookmarked, 
        composition_url,
        user_id, 
        user_name,
        is_user_followed, 
        user_slug) {
        $scope.interpretation.id = id;
        $scope.interpretation.title = title;
        $scope.interpretation.text = text;
        $scope.interpretation.is_admired = is_admired == 'True';
        $scope.interpretation.is_bookmarked = is_bookmarked == 'True';
        $scope.interpretation.composition = {
            'url': composition_url
        }
        $scope.interpretation.user = {
            'id': user_id,
            'name': user_name,
            'is_followed': is_user_followed == 'True',
            'slug': user_slug
        }

        getInterpretAssociates();
    };

    $scope.deleteInterpretation = function () {
        progress.hideProgress();

        confirmModalService.showDeleteConfirm().then(function () {
            interpretationModel.delete($scope.interpretation.id).then(function () {
                progress.hideProgress();
                window.location.href = '/@' + $scope.interpretation.user.slug;
            }, function () {
                progress.hideProgress();
                alert.showAlert('Currently unable to remove this draft');
            });
        });
    };

    $scope.showShare = function () {
        var share_url = window.location.href;
        var title = "'" + $scope.interpretation.title + "' by " + $scope.interpretation.user.name;
        var description = $scope.interpretation.text;
        var media = 'http://thirddime.com' + $scope.interpretation.composition.url;
        shareModalService.shareThisPage(share_url, title, description, media);
    };

    $scope.handleBookmark = function () {
        var interpretation = $scope.interpretation;

        if (interpretation.is_bookmarked) {
            bookService.unmarkInterpret(interpretation).then(function () {
                interpretation.is_bookmarked = false;
            });
        } else {
            bookService.bookmarkInterpret(interpretation).then(function () {
                interpretation.is_bookmarked = true;
            });;
        }
    };

    $scope.handleAdmire = function () {
        var interpretation = $scope.interpretation;

        if (interpretation.is_admired) {
            admireService.unadmireInterpret(interpretation).then(function () {
                interpretation.is_admired = false;
            });
        } else {
            admireService.admireInterpret(interpretation).then(function () {
                interpretation.is_admired = true;
            });;
        }
    };

    $scope.showBookMarkers = function () {
        usermodalService.showBookMarkers($scope.interpretation).then(function (bookStatus) {
            if (bookStatus == 'bookmarked') {
                $scope.interpretation.is_bookmarked = true;
            }
        });
    }

    $scope.showAdmirers = function () {
        usermodalService.showArtAdmirers($scope.interpretation).then(function (admireStatus) {
            if (admireStatus == 'admired') {
                $scope.interpretation.is_admired = true;
            }
        });
    }



    $scope.handleFollow = function (event) {
        var user = $scope.interpretation.user;

        if (user.is_followed) {
            followService.unfollow(user).then(function () {
                user.is_followed = false;
            });
        } else {
            followService.follow(user).then(function () {
                user.is_followed = true;
            });
        }
    }

    

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
});