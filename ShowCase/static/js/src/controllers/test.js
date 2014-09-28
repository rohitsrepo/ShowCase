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
    $scope.dummyNotes = [[{"x":0.4968017057569296,"y":0.22763063707945597,"note":"Position of sky like medivial works."}],[{"x":0.3784648187633262,"y":0.2612741589119542,"note":"Dali's signature way of painting tree. Strong and dry."}],[{"x":0.488272921108742,"y":0.30637079455977095,"note":"The age of Invention of God"},{"x":0.19936034115138593,"y":0.36721546170365066,"note":"Age of Empires"},{"x":0.8688699360341151,"y":0.25912670007158195,"note":"Age of Stone"},{"x":0.07356076759061833,"y":0.44738725841088045,"note":"Modern times"}]];
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
            element.html('<h1>Transformation of Life After <small>-Nikola</small></h1><p>   Like in a fable animals take place of people,here the elephants show that there is something after life,we die we get into dust but we leave something behind(the trees)that still lives from our ashes those swans are the things that we become after life from heavy and stuffy lifes here on earth to free and beautiful souls.anyway this is how i see the paint and it\'s a very beautiful one,full of metaphores<span ng-click="showNotes(dummyNotes, 2)"><sup>0</sup></span>.  Just to give this painting some history. This is from <a href="http://en.wikipedia.org/wiki/Dali">Dali\'s</a> "paraniod critical transformation method". <a href="http://www.dali-gallery.com/">Dali-gallery</a> says about this method:<blockquote>"It was defined by Dalí himself as "irrational knowledge" based on a "delirium of interpretation". More simply put, it was a process by which the artist found new and unique <span ng-click="showNotes(dummyNotes, 0)"><sup>1</sup></span> ways to view the world around him. It is the ability of the artist or the viewer to perceive multiple images within the same configuration. The concept can be compared to Max Ernst\'s frottage or Leonardo da Vinci\'s scribbling and drawings.</blockquote>As a matter of fact, all of us have practiced the Paranoid Critical Method when gazing at stucco on a wall, or clouds<span ng-click="showNotes(dummyNotes, 1)"><sup>2</sup></span> in the sky, and seeing different shapes and visages therein. Dalí elevated this uniquely human characteristic into his own artform." Do you think there is <a href="http://www.wikiwand.com/en/Symbolism">Symbolism</a> behind some of these images. Or was this just a way for Dali to blend the surreal with the real? I\'m mostly interested in symbolism behind art, so if you know of any other paintings of his, like the persistence of memory I\'d like to hear about that too. I think Dali was a twisted genius and I\'ve been fascinated by him and the events of his childhood that inspired his paintings.</p><br><br><h1>Act of Metaphores <small>-Albert</small></h1><p>   Like in a fable animals take place of people,here the elephants show that there is something after life,we die we get into dust but we leave something behind(the trees)that still lives from our ashes those swans are the things that we become after life from heavy and stuffy lifes here on earth to free and beautiful souls.anyway this is how i see the paint and it\'s a very beautiful one,full of metaphores<span ng-click="showNotes(dummyNotes, 2)"><sup>0</sup></span>.  Just to give this painting some history. This is from <a href="http://en.wikipedia.org/wiki/Dali">Dali\'s</a> "paraniod critical transformation method". <a href="http://www.dali-gallery.com/">Dali-gallery</a> says about this method:<blockquote>"It was defined by Dalí himself as "irrational knowledge" based on a "delirium of interpretation". More simply put, it was a process by which the artist found new and unique <span ng-click="showNotes(dummyNotes, 0)"><sup>1</sup></span> ways to view the world around him. It is the ability of the artist or the viewer to perceive multiple images within the same configuration. The concept can be compared to Max Ernst\'s frottage or Leonardo da Vinci\'s scribbling and drawings.</blockquote>As a matter of fact, all of us have practiced the Paranoid Critical Method when gazing at stucco on a wall, or clouds<span ng-click="showNotes(dummyNotes, 1)"><sup>2</sup></span> in the sky, and seeing different shapes and visages therein. Dalí elevated this uniquely human characteristic into his own artform." Do you think there is <a href="http://www.wikiwand.com/en/Symbolism">Symbolism</a> behind some of these images. Or was this just a way for Dali to blend the surreal with the real? I\'m mostly interested in symbolism behind art, so if you know of any other paintings of his, like the persistence of memory I\'d like to hear about that too. I think Dali was a twisted genius and I\'ve been fascinated by him and the events of his childhood that inspired his paintings.</p>')
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
