angular.module('module.root')
.controller('headerController', ['$scope',
    '$window',
    '$location',
    'auth',
    'uploadmodalService',
    'bucketmodalService',
    'activityModel',
    function ($scope,
        $window,
        $location,
        auth,
        uploadmodalService,
        bucketmodalService,
        activityModel)
    {

    $scope.exploreActive = false;
    $scope.homeActive = false;

    function initActiveLink() {
        path = window.location.pathname;

        if (path=='/arts') {
            $scope.exploreActive = true;
        } else if (path=='/home') {
            $scope.homeActive = true;
        }
    };
    initActiveLink();

    function transformRawNotification (notification) {
        var action, target_name, target_link;
        var verb = notification.verb;
        if (verb == 'IN') {
            action = "interpreted";
            target_name = notification.content_object.interpretation;
        }
        else if (verb == 'AD') {
            action = 'added new artwork';
            target_name = notification.content_object.title;
            target_link = '/arts/' + notification.content_object.slug;
        }
        else if (verb == 'CR') {
            action = 'contributed your artwork';
            target_name = notification.content_object.title;
            target_link = '/arts/' + notification.content_object.slug;
        }
        else if (verb == 'BK') {
            action = 'added artwork ' + notification.content_object.title + ' to series';
            target_name = '';
            target_link = '/arts/' + notification.content_object.slug;
        }
        else if (verb == 'MA') {
            action = 'admired artwork';
            target_name = notification.content_object.title;
            target_link = '/arts/' + notification.content_object.slug;
        }
        else if (verb == 'MB') {
            action = 'admired series';
            target_name = notification.content_object.name;
            target_link = '/@' + notification.content_object.owner.slug + '/series/' + notification.content_object.slug;
        }
        else if (verb == 'FL') {
            action = 'started following you';
            target_name = '';
            target_link = '/@' + $scope.user.slug;
        }
        else {
            console.error('Invalid notification activity type');
        }

        notification.action = action;
        notification.target_name = target_name;
        notification.target_link = target_link;

        return notification;
    };

    $scope.notifications = [];
    $scope.activeNotifications = {
        'status': false,
        'count': 0
    };

    var streamClient;

    function initStreamClient (user, feed_token) {
        streamClient = stream.connect('x399sdbsgtmx', null, '4933');
        var userFeed = streamClient.feed('notification', user.id, feed_token);

        function callback(data) {
            if (data.new.length == 0) {
                return;
            }

            // TODO: Delete the notifications that are coming deleted

            activityModel.enrichActivities(data.new).then(function(response) {
                var notification;
                for (var i = 0; i < response.length; i++) {
                    notification = transformRawNotification(response[i]);
                    $scope.notifications.unshift(notification);
                    if (!notification.is_seen) {
                        $scope.activeNotifications.status = true;
                        $scope.activeNotifications.count++;
                    }
                }
            });
        }

        function failCallback(data) {
            console.error(data);
        }

        userFeed.subscribe(callback).then(function(){}, failCallback);
    };

    var next_token;

    function getNotifications (user) {
        $scope.loadingNotifications = true;

        activityModel.notificationActivities(next_token).then(function (response) {

            $scope.loadingNotifications = false;

            var notification;
            for (var i = 0; i < response.results.length; i++) {
                notification = transformRawNotification(response.results[i]);
                $scope.notifications.push(notification);
                if (!notification.is_seen) {
                    $scope.activeNotifications.status = true;
                    $scope.activeNotifications.count++;
                }
            }

            next_token = response.next_token;

            if (!next_token) {
                $scope.noMoreNotifications = true;
            }

            if ($scope.notifications.length == 0) {
                $scope.noNotifications = true;
            }

            if (!streamClient && !$scope.noNotifications) {
                initStreamClient(user, response.feed_token);
            }

        }, function () {
            $scope.loadingNotifications = false;
        })
    };

    auth.getCurrentUser().then(function (user) {
        $scope.user = user;
        getNotifications(user);
    });

    $scope.showNotifications = function () {
        if (!$scope.activeNotifications.status) {
            return;
        }

        $scope.activeNotifications.status = false;
        $scope.activeNotifications.count = 0;

        // TODO send seen notification
        var activityIds = []
        for (var i = 0; i < $scope.notifications.length; i++) {
            activityIds.push($scope.notifications[i].id);
        }

        activityModel.markSeen(activityIds);
    };

    $scope.showMoreNotifications = function (event) {
        event.stopPropagation();
        if ($scope.loadingNotifications) {
            return;
        }

        getNotifications($scope.user);
    };

	$scope.authorize = function () {
		auth.runWithAuth();
	};

    $scope.showUpload = function () {
        uploadmodalService.showUpload();
    };

    $scope.goHome = function () {
        auth.getCurrentUser().then(function (user) {
            $window.location.href = '/@' + user.slug;
        });
    };

    $scope.gotoMySeries = function () {
        auth.getCurrentUser().then(function (user) {
            $window.location.href = '/@' + user.slug + '/series';
        });
    };

    $scope.gotoMyDrafts = function () {
        auth.getCurrentUser().then(function (user) {
            $window.location.href = '/@' + user.slug + '/drafts';
        });
    };

    $scope.gotoMyBookmarks = function () {
        auth.getCurrentUser().then(function (user) {
            $window.location.href = '/@' + user.slug + '/bookmarks';
        });
    };

    $scope.gotoMyContributions = function () {
        auth.getCurrentUser().then(function (user) {
            $window.location.href = '/@' + user.slug + '/contributions';
        });
    };

    $scope.showCreateBucket = function () {
        bucketmodalService.showCreateBucket();
    };

}])
.directive('customHref', [function () {
    return function (scope, element, attrs) {
        element.bind('click', function () {
            window.location.href = attrs['customHref'];
        })

    };
}])
.directive('siteLoader', [function () {
    return {
        restrict: 'E',
        replace: true,
        scope: {
            siteLoaderHide: '='
        },
        template: '<div class="site-loader" ng-cloak ng-hide="siteLoaderHide"><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span><span class="stick"></span></div>'
    };
}]);