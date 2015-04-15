angular.module("module.interpret")
.controller('interpretController', ['$scope', '$mdDialog', 'interpretationModel', 'compositionId', 
	function ($scope, $mdDialog, interpretationModel, compositionId) {
		$scope.cancel = function () {
			$mdDialog.cancel();
		}

		$scope.addInterpretation = function () {
			interpretationModel.addInterpretation(compositionId, $('textarea').val())
			.then(function () {
				$mdDialog.hide();
			});
		};
	}
]);
