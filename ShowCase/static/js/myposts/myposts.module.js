angular.module("MypostsApp", [
    "module.root"])
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
        requireBase: false
    });

    // Now set up the states
    $stateProvider
    .state('home', {
        url: "/home"
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
                    $state.go('home');
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
            'close': ['$state', function ($state) {
                return function () {
                    $state.go('home');
                };
            }]
        },
        data: {
            'isState' : true
        }
    });
}]);