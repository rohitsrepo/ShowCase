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

    // For any unmatched url, reload as we have not mentioned any base
    $urlRouterProvider.otherwise(
        function() {
            window.location.reload();

    });

    // use the HTML5 History API
    $locationProvider.html5Mode({
      enabled: true,
    });

    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/");
    //
    // Now set up the states
    $stateProvider
    .state('all', {
        url: "/",
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