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

    // For any unmatched url, reload as we have not mentioned any base
    $urlRouterProvider.otherwise(
        function() {
            window.location.reload();

    });

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
        url: "/originals",
        templateUrl: "/static/js/user/profile.paintings.html",
        controller: 'profilePaintingsController',
        data: {'listType': 'paintings'}
    })
    .state('uploads', {
        url: "/contributions",
        templateUrl: "/static/js/user/profile.paintings.html",
        controller: 'profilePaintingsController',
        data: {'listType': 'uploads'}
    })
    .state('bookmarks', {
        url: "/bookmarks",
        templateUrl: "/static/js/user/profile.artifacts.html",
        controller: 'profileArtifactsController',
        data: {'listType': 'bookmarks'}
    })
    .state('admirations', {
        url: "/admirations",
        templateUrl: "/static/js/user/profile.artifacts.html",
        controller: 'profileArtifactsController',
        data: {'listType': 'admirations'}
    })
    .state('buckets', {
        url: "/arts/{artSlug}/series",
        templateUrl: "/static/js/components/bucketmodal/bucketmodal.show.tpl.html",
        controller: 'bucketmodalShowController',
        resolve: {
            'art': ['$stateParams', 'compositionModel', function ($stateParams, compositionModel) {
                return compositionModel.getArt($stateParams.artSlug);
            }],
            'close': ['$state', function ($state) {
                return function () {
                    $state.go('activities');
                };
            }]
        }
    })
    .state('userbuckets', {
        url: "/series",
        templateUrl: "/static/js/user/profile.buckets.html",
        controller: 'profileBucketsController',
        data: {
            pageType: 'series'
        }
    })
    .state('userdrafts', {
        url: "/drafts",
        templateUrl: "/static/js/user/profile.buckets.html",
        controller: 'profileBucketsController',
        data: {
            pageType: 'drafts'
        }
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
        },
        data: {
            'isState' : true
        }
    });
}]);