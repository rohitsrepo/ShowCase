angular.module('module.root')
.controller('headerController', ['$scope',
    '$window',
    '$location',
    'auth',
    'uploadmodalService',
    'bucketmodalService',
    'activityModel',
    'searchModel',
    'progress',
    function ($scope,
        $window,
        $location,
        auth,
        uploadmodalService,
        bucketmodalService,
        activityModel,
        searchModel,
        progress)
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
            action = 'wrote a tale about ' + notification.target_object.title;
            target_name = '';
            target_link =  notification.content_object.url;
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
            action = 'added artwork ' + notification.target_object.title + ' to series';
            target_name = '';
            target_link = notification.content_object.url;
        }
        else if (verb == 'MA') {
            action = 'admired artwork';
            target_name = notification.content_object.title;
            target_link = '/@' + notification.actors[0].slug + '/admirations';
        }
        else if (verb == 'MB') {
            action = 'admired series';
            target_name = notification.content_object.name;
            target_link = '/@' + notification.actors[0].slug + '/admirations';
        }
        else if (verb == 'FL') {
            action = 'started following you';
            target_name = '';
            target_link = '/@' + notification.actors[0].slug;
        }
        else if (verb == 'AI') {
            action = 'admired your tale';
            target_name = '';
            target_link = '/@' + notification.actors[0].slug + '/admirations';
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
                    try {
                        notification = transformRawNotification(response[i]);
                    } catch (err) {
                        console.log('Notification parse error');
                        continue;
                    }
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
                try {
                    notification = transformRawNotification(response.results[i]);
                } catch (err) {
                    console.log('Notification parse error');
                    continue;
                }
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

    $scope.search = {};
    $scope.search.results = {
        'users': [],
        'buckets': [],
        'arts': [],
        'show': false,
        'count': 0
    };

    $scope.search.loading = false;
    $scope.search.noresults = false;

    var search = function (query) {
        progress.showProgress();
        $scope.search.results = {
            'users': [],
            'buckets': [],
            'arts': [],
            'show': false,
            'count': 0
        };

        $scope.search.loading = true;
        $scope.search.noresults = false;
        $scope.search.results.show = true;

        searchModel.search(query).then(function (results) {

            for (i=0; i< results.results.length; i++) {
                var result = results.results[i];
                $scope.search.results.count++;

                if (result.content_type == 'user') {
                    if ($scope.search.results.users.length == 3) {
                        continue;
                    }

                    $scope.search.results.users.push(result.content_object)
                }else if (result.content_type == 'bucket') {
                    if ($scope.search.results.buckets.length == 3) {
                        continue;
                    }

                    $scope.search.results.buckets.push(result.content_object)
                }else if (result.content_type == 'composition') {
                    if ($scope.search.results.arts.length == 3) {
                        continue;
                    }

                    $scope.search.results.arts.push(result.content_object)
                }
            }

            progress.hideProgress();
            $scope.search.loading = false;
            if (results.results.length == 0) {
                $scope.search.noresults = true;
            }

        }, function () {
            progress.hideProgress();
            $scope.search.loading = false;
            $scope.search.noresults = false;
        });
    };

    $scope.$watch(function () {
        return $scope.search.query;
    }, function (val) {
        if (!val) {
            return;
        }

        search(val);
    })

    $scope.hideSearchResults = function () {
        $scope.search.results.show = false;
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
        template: '<span class="site-loader" ng-cloak ng-hide="siteLoaderHide"><span class="site-loader-inner"></span></span>'
    };
}])
.directive('clickCloseSearch', ['$document', function ($document) {
    return function (scope, element, attrs) {
        $document.bind('click', function (event) {
            var isClickedInside = element.find(event.target).length > 0 || element[0] == event.target;
            if (!isClickedInside) {
                scope.hideSearchResults();
            }
        });
    };
}]);