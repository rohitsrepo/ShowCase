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
    $locationProvider.html5Mode(true);

    // Now set up the states
    $stateProvider
    .state('art', {
        url: "/arts/{compositionSlug}"
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
                    console.log("calling here");
                    $state.go('arts');
                };
            }]
        }
    });
}]);