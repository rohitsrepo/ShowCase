var testCtrlModule = angular.module('controller.test', ['angularFileUpload', 'ngSanitize']);

testCtrlModule.factory('imgNotes', function ($sce) {
    var service = {};
    service.editorText = $sce.trustAsHtml('<h1>This is where <button ng-click="showNotes()"><sup>0</sup></button> editor goes.h</h1> ');

    // Edit releate functionaliy and state.
    service.isBeingEdited = false;
    service.addedNotesCount = 0;
    service.addedNotes = [];

    service.initNotesWithedit = function () {
        try{
            service.imageElement.imgNotes("destroy");
        } catch (err) {}
        
        service.imageElement.imgNotes();
        console.log('Logging the first of notes: ', service.imageElement);
        var imgNote2 = service.imageElement.imgNotes("option", "canEdit", true);
        console.log('Logging the first of notes: ', imgNote2);
        service.isBeingEdited = true;
    }

    service.disableNotesEdit = function () {
        service.imageElement.imgNotes("option", "canEdit", false);                
        service.isBeingEdited = false;
        var count = service.addedNotesCount;
        service.addedNotes[count] = service.imageElement.imgNotes('export');
        service.addedNotesCount = service.addedNotesCount + 1;
    }

    service.addNote = function (posX, posY, noteText) {
        return service.imageElement.imgNotes('addNote', posX, posY, noteText);
    }

    // Display related functionality. Try not to keep any state here
    // Might collide with ongoing edit session.

    service.showNotes = function (imageElement, notes) {
        try{
            service.imageElement.imgNotes("destroy");
        } catch (err) {}
        
        imageElement.imgNotes();
        imageElement.imgNotes('import', notes);
        return imageElement.imgNotes('getNotes');
    }

    //Rough
    service.testNotes = [   {x: "0.5", y:"0.5", note:"AFL Grand Final Trophy"}, 
                            {x: "0.322", y:"0.269", note: "Brisbane Lions Flag"},
                            {x: "0.824", y: "0.593", note: "Fluffy microphone"}];


    return service;
});

testCtrlModule.controller('testCtrl', ['$scope', '$upload', 'imgNotes', function ($scope, $upload, imgNotes) {
    $scope.zoomeOptions = {hoverEf: 'grayscale', showZoomState: true, zoomRange: [1, 5], zoomStep: 0.5, defaultZoom: 1.5, magnifierSize: [200, 200], borderSize: 1000};
    $scope.editorText = imgNotes.editorText;
    $scope.dummyNotes = [[{"x":0.4968017057569296,"y":0.22763063707945597,"note":"These are eyes are so deep man."}],[{"x":0.3784648187633262,"y":0.2612741589119542,"note":"Same bone structure as Vinci's self potrait.\nhttp://upload.wikimedia.org/wikipedia/commons/8/8e/DaVinci_MonaLisa1b.jpg\n"}],[{"x":0.488272921108742,"y":0.30637079455977095,"note":"The interesting points.\n1> The smile"},{"x":0.19936034115138593,"y":0.36721546170365066,"note":"The interesting points.\n\n2> The water flow"},{"x":0.8688699360341151,"y":0.25912670007158195,"note":"The interesting points.\n\n\n3> The Horizon"},{"x":0.07356076759061833,"y":0.44738725841088045,"note":"The interesting points.\n\n\n\n\n4> These rock formations."}]];
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
        restrict: 'E',
        scope: {
            zoomeOptions: '='
        },
        link : function (scope, element, attrs) {
            console.log("Zoome options: ", scope.zoomeOptions);
            var imageElem = element.find("#image");
            console.log("Zoome element: ", imageElem);
            console.log("Zoome element old:", element.find());

            imageElem.zoome(scope.zoomeOptions);
            
            scope.$watch('zoomeOptions', function (newVal, oldVal) {
                if (newVal === oldVal){
                    return;
                }
                console.log('sensing a change in the zoomeOptions: ', newVal);
                if(imageElem.parent().hasClass('zm-wrap')){
                    imageElem.unwrap().next().remove();
                }
                
                imageElem.zoome(newVal);
            }, true);

            var editButton = element.find("#togglevfinder");
            editButton.bind("click", function () {
                if (editButton.text() == "DisableV"){
                    if(imageElem.parent().hasClass('zm-wrap')){
                        console.log("Ready to disable zoome.");
                        imageElem.unwrap().next().remove();
                    }
                    editButton.text("EnableV");
                } else {
                    editButton.text("DisableV");
                    console.log("Re-inti zoome with options: ", scope.zoomeOptions);
                    if(imageElem.parent().hasClass('zm-wrap')){
                        console.log("Ready to disable zoome.");
                        imageElem.unwrap().next().remove();
                    }
                    imageElem.zoome(scope.zoomeOptions);
                }
            });
        }
    }
});

testCtrlModule.directive('zoomeold', function () {
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
        link: function (scope, element, attrs) {
            var childImages = element.find("#image");
            scope.element = childImages;
            $log.info('initialized the directive on element: ', scope.element);
            childImages.imgNotes();
            childImages.imgNotes("import", [   {x: "0.5", y:"0.5", note:"AFL Grand Final Trophy"}, 
                                    {x: "0.322", y:"0.269", note: "Brisbane Lions Flag"},
                                    {x: "0.824", y: "0.593", note: "Fluffy microphone"}]);

            

            var exportButton = element.find("#export");
            exportButton.bind("click", function() {
                var notes = childImages.imgNotes('export');
                $log.info('Data to be exported: ', notes);
            })

            scope.name= "Rohit";

            var testNote = childImages.imgNotes('addNote', "0.824", "0.824", "This is a test note.");
            console.log("This is a test note: ", testNote);

            scope.tsetFun = function () {
                console.log("Reached the right function");
                testNote.onclick();
            }

            var editButton = element.find("#toggleEdit");
            editButton.bind("click", function () {
                if (editButton.text() == "Edit"){
                    childImages.imgNotes("option", "canEdit", true);
                    editButton.text("View");
                } else {
                    editButton.text("Edit");
                    childImages.imgNotes("option", "canEdit", false);
                }
            });

            var createButton = element.find("#toggleCreate");
            createButton.bind("click", function () {
                if (createButton.text() == "Disable"){
                    console.log("Here to destroy image notes");
                    childImages.imgNotes("destroy");
                    editButton.hide();
                    createButton.text("Enable");
                } else {
                    childImages.imgNotes();
                    childImages.imgNotes("import", [   {x: "0.5", y:"0.5", note:"AFL Grand Final Trophy"}, 
                                    {x: "0.322", y:"0.269", note: "Brisbane Lions Flag"},
                                    {x: "0.824", y: "0.593", note: "Fluffy microphone"}]);
                    editButton.show();
                    createButton.text("Disable");
                }
            });
        }
    }
});

testCtrlModule.directive("testscope", function () {
    return {
        restrict: 'E',
        scope : {

        },
        template : '<button ng-click="testFun()">{{testVal}}</button>',
        link: function (scope) {
            scope.testVal = "Rohit";
            scope.testFun = function () {
                alert("Here I am");
            }
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

testCtrlModule.directive('medium', function ($sce, $interval, imgNotes) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var testButton = new MediumButton({
                label: 'Test',
                action: function (html, mark) {
                    imgNotes.initNotesWithedit();
                    html = html + ' <span ng-click="showNotes(dummyNotes)"><sup>' + imgNotes.addedNotesCount + '</sup></span>';
                    console.log("init notes with edit done", imgNotes.addedNotesCount);

                    var inter = $interval(function () {
                        console.log("ooking for edit to stop");
                        if (!imgNotes.isBeingEdited){
                            stopLookingForEdit();
                            console.log("Looks like it finally stopped");
                        }
                    }, 500);

                    var stopLookingForEdit = function () {
                        $interval.cancel(inter)
                    }

                    return html;
                }
            });
            var editor = new MediumEditor(element, {
                buttons: ['bold', 'italic', 'underline', 'anchor', 'header1', 'header2', 'quote','Test'],
                extensions: {
                    'Test': testButton
                }
            });

            element.on('input', function () {
                scope.$apply(function () {
                    imgNotes.editorText = editor.serialize()['editable-div'].value;
                    scope.addedNotes = imgNotes.addedNotes;
                    console.log("Notes added to service: ", imgNotes.addedNotes);
                });
                console.log('what we have so far: ', imgNotes.editorText);
            })
        }
    }
});

testCtrlModule.directive('showMedium', function ($compile) {
    return {
        restrict: "EA",
        link: function (scope, element, attrs) {
            element.html('<h1>The art itself.</h1><p>It has been argued that the Mona Lisa is a self-portrait <a href="http://en.wikipedia.org/wiki/Leonardo_da_Vinci">Da Vinci</a> created in order to portray himself as a woman. Research and analysis by <a href="http://en.wikipedia.org/wiki/Lillian_Schwartz\">Dr. Lillian F. Schwartz</a> shows that the faces of a self-portrait by Da Vinci and the Mona Lisa line up using digital scanning to reverse and overlay the portraits. The facial features match perfectly, so one could assume that Mona Lisa is not actually a woman at all, but <b>Da Vinci’s portrayal <span ng-click="showNotes(dummyNotes, 1)"><sup>1</sup></span> of himself as a woman.</b></p><blockquote>“Mona Lisa only has eyes <span ng-click="showNotes(dummyNotes, 0)"><sup>0</sup></span> for me. There is no other. No one more interesting, more intelligent, more compelling. And what is extraordinary, if a dozen others crowd into this room, each one will feel the same. Each person who looks at her becomes the only person in her world. It is flattering and, at the same time, maddening, because she gives away nothing of herself.”&nbsp;</blockquote><p>This painting has become one of the most famous and symbolic paintings in the world, yet one has to wonder why. What was so mysterious about this particular work that caused the world to throw it into such scrutinous speculation? Why must we define this particular work as a political or meaningful statement? While there are some very interesting <span ng-click="showNotes(dummyNotes, 2)"><sup>2</sup></span> aspects to this work, we will never truly know the meaning and motivation for Da Vinci to make this portrait. Yet we continue to search for answers, so we may be more comfortable with this artwork. This is very unlike other classical works of art, such as that of Frida Kahlo (discussed earlier in the blog). We take Kahlo\'s work for what it is, very little interpretations or accusations of meaning are placed onto her artwork, yet we are still able to learn from it. It is interesting that we are not able to do this for the Mona Lisa as well.</p>  ')
            $compile(element.contents())(scope);
        }
    }
});

testCtrlModule.directive('forClick', function () {
    return {
        restrict: 'AE',
        link: function (scope, element, attrs) {
            element.on('click', function () {
                console.log("Yup, this dude was clicked");
            })
        }
    }
});
testCtrlModule.directive('imageDisplay', function (imgNotes) {
    return {
        restrict: 'E',
        transclude: true,
        template: '<div ng-transclude> </div>',
        link: function (scope, element, attrs) {

            // Image Notes.
            var imageElement = element.find("img");
            imgNotes.imageElement = imageElement;
            scope.disableNotesEdit = imgNotes.disableNotesEdit;
            scope.showNotes = function (notes, index) {
                console.log("Lets show some notes");
                imgNotes.showNotes(imageElement, notes[index]);
            }

            // Zoome.
            scope.zoomeOptions = {hoverEf: 'grayscale', showZoomState: true, zoomRange: [1, 5], zoomStep: 0.5, defaultZoom: 1.5, magnifierSize: [200, 200], borderSize: 1000};
            //imageElement.zoome(scope.zoomeOptions);
            scope.disableViewFinderButtonText = "Disable ViewFinder";
            scope.disableViewFinder = function () {
                if (scope.disableViewFinderButtonText == 'Disable ViewFinder'){
                    if(imageElement.parent().hasClass('zm-wrap')){
                        imageElement.unwrap().next().remove();
                    }
                    scope.disableViewFinderButtonText = 'Enable ViewFinder';
                } else {
                    imageElement.zoome(scope.zoomeOptions);
                    scope.disableViewFinderButtonText = 'Disable ViewFinder';
                }
            }

            //var testNote = imageElement.imgNotes('addNote', "0.824", "0.824", "This is a test note.");
            scope.testNoteFun = function () {
                testNote.click();
                testNote.css({color: "#000"});
            }
        }
    }
});
