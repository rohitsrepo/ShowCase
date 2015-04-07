angular.module('module.curtainRight', ["module.auth" , "ngFacebook", "module.model"])

.config(['$facebookProvider', function( $facebookProvider ) {
  $facebookProvider.setAppId('543342382357619').setPermissions(['email','user_friends']);
}])

.run(['$rootScope','$window', function( $rootScope, $window ) {
  // Cut and paste the "Load the SDK" code from the facebook javascript sdk page.
  
  // Load the facebook SDK asynchronously
    (function(d, s, id){
         var js, fjs = d.getElementsByTagName(s)[0];
         if (d.getElementById(id)) {return;}
         js = d.createElement(s); js.id = id;
         js.src = "//connect.facebook.net/en_US/sdk.js";
         fjs.parentNode.insertBefore(js, fjs);
       }(document, 'script', 'facebook-jssdk'));
    $rootScope.$on('fb.load', function() {
      $window.dispatchEvent(new Event('fb.load'));
  });
}]);

