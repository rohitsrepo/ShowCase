angular.module("SearchApp", [
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
    $locationProvider.html5Mode({
      enabled: true,
    });

    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/all");
    //
    // Now set up the states
    $stateProvider
    .state('all', {
        url: "/all",
        templateUrl: "/static/js/search/search.all.html",
        controller: 'searchAllController'
    })
    .state('arts', {
        url: "/artworks",
        templateUrl: "/static/js/search/search.all.html",
        controller: 'searchAllController'
    })
    .state('buckets', {
        url: "/series",
        templateUrl: "/static/js/search/search.all.html",
        controller: 'searchAllController'
    })
    .state('users', {
        url: "/people",
        templateUrl: "/static/js/search/search.all.html",
        controller: 'searchAllController'
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