angular.module("module.curtainRight")
.controller('rightCurtainController', ['$scope', "auth", "$location", "$facebook", function ($scope, auth, $location, $facebook) {
	'use strict';

	$scope.login = function (user) {
		auth.login(user.email, user.password, $location.absUrl()).then(function (response) {
			$scope.loginError = '';
		}, function (error) {
			$scope.loginError = error;
		});
	};

	function loginUserWithFacebook () {
		$facebook.api('/me').then( function(response) {
    		$scope.user = response;
    		var userObject=
   			{
   				first_name: response.first_name,
   				last_name: response.last_name,
   				login_type: "FB",
   				email: response.email,
   				password: "" 
   			};	
   			auth.registerUser(userObject).then(function(response){
				$scope.loginError = '';
				}, function (error) {
				$scope.loginError = error;
			});
       	});
	};

    $scope.loginFB = function() {
        $facebook.getLoginStatus().then(function(response) {
	        if(response.status === 'connected') {
       			loginUserWithFacebook();
	        } else {
	        	$facebook.login().then(function(response) {
	        		if (response.status != 'connected') {
	        			return;
	        		} 
	        		loginUserWithFacebook();
		        });
	        }		
	      });
	    };

}]);