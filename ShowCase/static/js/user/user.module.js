angular.module("UserApp", [
    "lr.upload",
    'ui.router',
    "module.root"])
.config(['$httpProvider',
 '$interpolateProvider',
 '$stateProvider',
 '$urlRouterProvider',
 '$locationProvider',
  function ($httpProvider, $interpolateProvider, $stateProvider, $urlRouterProvider, $locationProvider) {
    "use strict";

    // Changing angular template tag to prevent conflict with django
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]')

    // csrf for django
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';

    // use the HTML5 History API
    $locationProvider.html5Mode(true);

    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/activities");
    //
    // Now set up the states
    $stateProvider
    .state('activities', {
        url: "/activities",
        templateUrl: "/static/js/user/profile.activities.html",
        controller: 'profileActivitiesController'
    })
    .state('paintings', {
        url: "/paintings",
        templateUrl: "/static/js/user/profile.paintings.html",
        controller: 'profilePaintingsController',
        data: {'listType': 'paintings'}
    })
    .state('uploads', {
        url: "/uploads",
        templateUrl: "/static/js/user/profile.paintings.html",
        controller: 'profilePaintingsController',
        data: {'listType': 'uploads'}
    })
    .state('bookmarks', {
        url: "/admirations",
        templateUrl: "/static/js/user/profile.paintings.html",
        controller: 'profilePaintingsController',
        data: {'listType': 'bookmarks'}
    })
    .state('buckets', {
        url: "/series",
        templateUrl: "/static/js/user/profile.buckets.html",
        controller: 'profileBucketsController'
    })
    .state('bucket', {
        url: "/series/{bucketSlug}",
        templateUrl: "/static/js/components/bucketmodal/bucketmodal.content.tpl.html",
        controller: 'bucketmodalContentController',
        resolve: {
            'bucket': ['$stateParams', 'bucketModel', function ($stateParams, bucketModel) {
                return bucketModel.getBucket($stateParams.bucketSlug);
            }],
            'close': ['$state', function ($state) {
                return function () {
                    $state.go('buckets');
                };
            }]
        }
    });
}]);