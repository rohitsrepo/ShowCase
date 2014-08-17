var testCtrlModule = angular.module('controller.test', ['angularFileUpload']);

testCtrlModule.controller('testCtrl', ['$scope', '$upload', function ($scope, $upload) {
    console.log('Test controller initialized');
    $scope.zoomeOptions = {hoverEf: 'grayscale', showZoomState: true, zoomRange: [1, 5], zoomStep: 0.5, defaultZoom: 1.5, magnifierSize: [200, 200], borderSize: 1000};
    $scope.notesButtonLable = "This is a buttttaaaannnnnn..";
}]);

testCtrlModule.directive('elevatez', function () {
    return {
        restrict: 'A',
        scope: {
            option: "="
        },
        link: function (scope, element, attrs) {
            console.log('calling the elevateZoom', scope.option);
            element.elevateZoom(scope.option);
        }
    }
});

testCtrlModule.directive('shoot', function () {
    return {
        restrict: 'E',
        link: function (scope, element, attrs) {
            var config = {
                image : '/static/img/callout.jpg',
                blurLevel	: 6,
                opacity	: 0.8
                    };

            element.photoShoot(config);
        }
    }
});

testCtrlModule.directive('zoome', function () {
    return {
        restrict: 'A',
        scope: {
            zoomeOptions: '='
        },
        link : function (scope, element, attrs) {
            console.log("Zoome options: ", scope.zoomeOptions);
            console.log("Zoome element: ", element);
            element.zoome(scope.zoomeOptions);
            
            scope.$watch('zoomeOptions', function (newVal, oldVal) {
                if (newVal === oldVal){
                    return;
                }
                console.log('sensing a change in the zoomeOptions: ', newVal);
                if(element.parent().hasClass('zm-wrap')){
                    element.unwrap().next().remove();
                }
                
                element.zoome(newVal);
            }, true);
        }
    }
});

testCtrlModule.directive('notes', function ($log) {
    return {
        restrict: 'E',
        scope: {},

        controller: function ($scope) {
            $scope.element = '';

            this.editorButton = function (){

            }
        },
        link: function (scope, element, attrs) {
            var childImages = element.find("#image");
            scope.element = childImages;
            $log.info('initialized the directive on element: ', element);
            childImages.imgNotes();
            childImages.imgNotes("import", [   {x: "0.5", y:"0.5", note:"AFL Grand Final Trophy"}, 
                                    {x: "0.322", y:"0.269", note: "Brisbane Lions Flag"},
                                    {x: "0.824", y: "0.593", note: "Fluffy microphone"}]);

            var exportButton = element.find("#export");
            exportButton.bind("click", function() {
                var notes = childImages.imgNotes('export');
                $log.info('Data to be exported: ', notes);
            })

            var editButton = element.find("#toggleEdit");
            editButton.bind("click", function () {
                if (editButton.text() == "Edit"){
                    editButton.text("View");
                    childImages.imgNotes("option", "canEdit", true);
                } else {
                    editButton.text("Edit");
                    childImages.imgNotes("option", "canEdit", false);
                }
            });
        }
    }
});

testCtrlModule.directive('editorButton', function () {
    return {
        restrict: 'A',
        require: '^notes',
        link: function (scope, element, attrs, notesCtrl) {
            console.log('Got to editorbutton on element: ', element);
            element.bind("mouseenter", function () {
                console.log("got clicked.", element);
                notesCtrl.editorButton();
            });
        }
    }
});