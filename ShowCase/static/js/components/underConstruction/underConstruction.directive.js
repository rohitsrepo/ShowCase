angular.module('module.underConstruction', ['ngMaterial'])
.directive('underConstruction', ['$mdDialog', function ($mdDialog) {
    return function (scope, element, attrs) {
        element.bind('click', function (event) {
            $('.curtain-overlay-placeholder').click();
            $mdDialog.show({
                targetEvent: event,
                templateUrl: '/static/js/components/underConstruction/underConstruction.tpl.html',
                controller: 'constructionController',
                disableParentScroll: false
            });
        });
    }
}]);