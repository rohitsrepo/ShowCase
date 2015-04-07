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

	$scope.fb_login = function() {
      // From now on you can use the Facebook service just as Facebook api says
      $facebook.login().then(function(response) {
        // Do something with response.
        console.log('Successful login for:',response);
      });
    };

    $scope.getLoginStatus = function() {
      $facebook.getLoginStatus().then(function(response) {
        if(response.status === 'connected') {
       			$facebook.api('/me').then( function(response) {
        		$scope.user = response;
        		var userObject=
       			{
       				first_name: response.first_name,
       				login_type: "facebook",
       				email: response.email,
       				password: "" 
       			};	
       			console.log('Successful login for: ', userObject);
       			auth.registerUser(userObject).then(function(response){
					$scope.loginError = '';
					}, function (error) {
					$scope.loginError = error;
				});
       	});

        } else {
        	$facebook.login().then(function(response) {
        		// Do something with response.
        		$facebook.api('/me').then( function(response) {
        		$scope.user = response;
        		var userObject=
       			{	
       				first_name: response.first_name,
       				login_type: "facebook",
       				email: response.email,
       				password: "" 
       			};
        		console.log('Successful login for: ', userObject);
       			auth.registerUser(userObject).then(function(response){
					$scope.loginError = '';
					}, function (error) {
					$scope.loginError = error;
				});
       		});
          });
        }		
      });
    };

    $scope.me = function() {
      $facebook.api('/me', function(response) {
        $scope.user = response;
        console.log('Successful login for: ' + response.name);
      });
    };

}]);