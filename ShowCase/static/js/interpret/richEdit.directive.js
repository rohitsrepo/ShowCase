angular.module("InterpretApp")
.directive('richEdit', ['$interval', function ($interval) {
	return function (scope, element, attts) {

		var editorOptions = {
			'buttons': ['bold', 
				'italic', 'anchor', 'header1', 'quote', 'justifyLeft', 'justifyCenter', 'justifyRight'],
			'anchorInputPlaceholder' : 'Enter complete link',
			'targetBlank': true,
			'placeholder': 'Start writing here...',
			'checkLinkFormat': true,
			'disableAnchorPreview': false,
            'buttonLabels': 'fontawesome',
			'imageDragging': false,
			// extensions: {
			//     'image': new ImageExtension({'scope': scope})
			// }
		};

		var editor = new MediumEditor(element, editorOptions);
	};
}])