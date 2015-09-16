angular.module("CompositionApp", [
    'ngSanitize',
    'infinite-scroll',
    'module.root',
    'module.tools'])
.value('$anchorScroll', angular.noop)
.config(['$httpProvider',
    '$interpolateProvider',
    '$urlRouterProvider',
    '$stateProvider',
    '$locationProvider',
    function ($httpProvider, $interpolateProvider, $urlRouterProvider, $stateProvider, $locationProvider) {
    "use strict";

    // Changing angular template tag to prevent conflict with django
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    // csrf for django
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';

    // use the HTML5 History API
    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
    });

    // Now set up the states
    $stateProvider
    .state('art', {
        url: "/arts/{compositionSlug}"
    })
    .state('buckets', {
        url: "/arts/{compositionSlug}/series",
        templateUrl: "/static/js/components/bucketmodal/bucketmodal.show.tpl.html",
        controller: 'bucketmodalShowController',
        resolve: {
            'art': ['$stateParams', 'compositionModel', function ($stateParams, compositionModel) {
                return compositionModel.getArt($stateParams.compositionSlug);
            }],
            'close': ['$state', '$stateParams', function ($state, $stateParams) {
                return function () {
                    $state.go('art', {'compositionSlug': $stateParams.compositionSlug});
                };
            }]
        }
    })
    .state('bucket', {
        url: "/@{userSlug}/series/{bucketSlug}",
        templateUrl: "/static/js/components/bucketmodal/bucketmodal.content.tpl.html",
        controller: 'bucketmodalContentController',
        resolve: {
            'bucket': ['$stateParams', 'bucketModel', function ($stateParams, bucketModel) {
                return bucketModel.getBucket($stateParams.bucketSlug);
            }],
            'close': ['$window', function ($window) {
                return function () {
                    $window.history.back();
                };
            }]
        },
        data: {
            'isState' : true
        }
    });
}]);