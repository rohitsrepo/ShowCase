angular.module("module.interpret")
.directive('richEdit', ['$interval', function ($interval) {
	return function (scope, element, attts) {

		var editorOptions = {
			'buttons': ['bold', 'italic', 'anchor', 'header1', 'header2', 'quote'],
			'anchorInputPlaceholder' : 'Enter complete link',
			'targetBlank': true,
			'placeholder': 'Enter text here',
			'checkLinkFormat': true,
			'disableAnchorPreview': false
		};

		var editor = new MediumEditor(element, editorOptions);
	};
}]);