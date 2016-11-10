angular.module('UserApp')
.controller('userProfileController', ['$scope', 'followService', 'usermodalService', 'alert', 'progress', function ($scope, followService, usermodalService, alert, progress) {
	$scope.hideName = true;
	$scope.artist = {'is_followed': false};

	$scope.init = function (id, is_followed, is_me, picture_major) {
        $scope.artist.id = id;
        $scope.artist.is_followed = is_followed == 'True';
        $scope.artist.is_me = is_me == 'True';
        $scope.artist.picture_major = picture_major;
        addColor(picture_major);
	};

    function addColor(color) {
        var header = document.querySelector('.primary-header');
        var siteHeader = document.querySelector('.site-header');
        var progressBar = document.querySelector('.progress-bar');

        var textColor = getTextColor(color);
        if (textColor == 'white') {
            header.className += " white";
            siteHeader.className += " white";
            progressBar.className += " white";
        }

        var circularEffectNode = document.createElement('section');
        circularEffectNode.className = 'circleEffect';
        var picture = document.querySelector('.picture');
        var bounds = picture.getBoundingClientRect();
        circularEffectNode.style.left = bounds.left + bounds.width / 2 + 'px';
        circularEffectNode.style.top = bounds.top + bounds.height / 2 + 'px';
        header.appendChild(circularEffectNode);

        circularEffectNode.style.background = color;
        var scaleSteps = [{transform: 'scale(0)'}, {transform: 'scale(1)'}];
        var timing = {duration: 800, easing: 'ease-in-out'};
        var scaleEffect = new KeyframeEffect(circularEffectNode, scaleSteps, timing);
        var allEffects = [scaleEffect];

        // Play all animations within this group.
        var groupEffect = new GroupEffect(allEffects);
        var anim = document.timeline.play(groupEffect);
        anim.addEventListener('finish', function() {
          header.style.backgroundColor = color;
          siteHeader.style.backgroundColor = color;
          header.removeChild(effectNode);
        });
    };

    function getTextColor(color) {
        var red = parseInt(color.substring(1,3), 16);
        var green = parseInt(color.substring(3,5), 16);
        var blue = parseInt(color.substring(5), 16);

        var lum = 1 - ( 0.299 * red + 0.587 * green + 0.114 * blue)/255;

        if (lum > 0.5){
            return 'white';
        }

        return 'black';
    }

	$scope.handleFollow = function () {
        var artist = $scope.artist;

		if (artist.is_followed) {
			followService.unfollow(artist).then(function () {
                artist.is_followed = false;
            });
		} else {
			followService.follow(artist).then(function () {
                artist.is_followed = true;
            });
		}
	};

    $scope.showFollows = function () {
        usermodalService.showFollows($scope.artist);
    };

    $scope.showFollowers = function () {
        usermodalService.showFollowers($scope.artist).then(function (followStatus) {
            if (followStatus == 'followed') {
                $scope.artist.is_followed = true;
            }
        });
    };
}]);