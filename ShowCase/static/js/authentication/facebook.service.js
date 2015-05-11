angular.module('module.auth')
.factory("facebook", ['$facebook', 'auth', function ($facebook, auth) {

    function loginUserWithFacebook (next_url) {
        $facebook.api('/me').then( function(userFB) {
            var userObject=
            {
                name: (userFB.first_name + " " + userFB.last_name).trim(),
                login_type: "FB",
                email: userFB.email,
                password: "" 
            };

            return auth.registerUser(userObject, (next_url || '/'));
        });
    };

    var service = {};

    service.login = function(next_url) {
      return $facebook.getLoginStatus().then(function(response) {
            if(response.status === 'connected') {
                return loginUserWithFacebook(next_url);
            } else {
                $facebook.login().then(function(response) {
                        if (response.status != 'connected') {
                            return;
                        } 
                        return loginUserWithFacebook(next_url);
                });
            }       
        });
    };

    return service;
}]);