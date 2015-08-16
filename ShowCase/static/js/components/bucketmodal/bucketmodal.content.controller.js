angular.module('module.bucketmodal')
.controller('bucketmodalContentController', ['$scope',
    'bucketModel',
    'bucketmodalService',
    'close',
    'KeydownCallback',
    'bucket',
    'progress',
    'alert',
    function ($scope, bucketModel, bucketmodalService, close, KeydownCallback, bucket, progress, alert) {

        progress.showProgress();
        $scope.bucket = bucket;

        bucketModel.bucketArts(bucket.id).then(function (arts) {
            $scope.bucketArts = arts;

            if ($scope.bucketArts.length > 2){
                $scope.bucketArts.push({
                    matter_aspect: 1
                })
            }

            progress.hideProgress();
        }, function () {
            alert.showAlert('We are unable to art for this series');
            progress.hideProgress();
        });

        $scope.KeydownCallback = KeydownCallback;

        $scope.close = function () {
            close();
        };

    }
])
.directive('horizontalSly', ['$timeout', function ($timeout) {
    return function (scope, element, attrs) {


        scope.$on('slyLastElement', function () {

            var sly;

            // Call Sly on frame
            $timeout(function () {

                var $slidee = element.children().eq(0);
                var $wrap   = element.parent();

                sly = new Sly(element, {
                    horizontal: 1,
                    itemNav: 'centered',
                    smart: 1,
                    activateOn: 'click',
                    mouseDragging: 1,
                    touchDragging: 1,
                    releaseSwing: 1,
                    startAt: 0,
                    scrollBar: $wrap.find('.scrollbar'),
                    scrollBy: 1,
                    activatePageOn: 'click',
                    speed: 300,
                    elasticBounds: 1,
                    easing: 'easeOutExpo',
                    dragHandle: 1,
                    dynamicHandle: 1,
                    clickBar: 1,

                    // Buttons
                    prev: $wrap.find('.prev'),
                    next: $wrap.find('.next')
                }).init();
            }, 0);

            scope.KeydownCallback(function (evt) {
                if (evt.keyCode == 37) {
                    sly.prev();
                }

                if (evt.keyCode == 39) {
                    sly.next();
                }

            });


        });
    };

}])
.directive('checkLast', [function () {

    return function (scope, element, attrs) {
        if (scope.$last) {
            scope.$emit('slyLastElement')
        }
    };
}]);