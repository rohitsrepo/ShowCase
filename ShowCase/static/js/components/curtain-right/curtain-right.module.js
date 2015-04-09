angular.module('module.curtainRight', ["module.auth", "ngFacebook"])
.config(['$facebookProvider', function( $facebookProvider ) {
  $facebookProvider.setAppId('462422103909005').setPermissions(['email']);
}])
.run(['$rootScope','$window', function( $rootScope, $window ) {
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