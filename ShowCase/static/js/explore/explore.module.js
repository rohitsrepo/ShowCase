angular.module("ExploreApp", ['ui.router',
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

    // use the HTML5 History API
    $locationProvider.html5Mode(true);

    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/arts");
    //
    // Now set up the states
    $stateProvider
    .state('arts', {
        url: "/arts",
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
                    $state.go('arts');
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
                    $state.go('arts');
                };
            }]
        }
    });
}]);