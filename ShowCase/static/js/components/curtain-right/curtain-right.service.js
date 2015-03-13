angular.module("module.curtainRight")
.factory("curtainRight", 
    ['$q', '$templateCache', '$http', '$rootScope', '$compile', '$document', '$timeout',
    function ($q, $templateCache, $http, $rootScope, $compile, $document, $timeout) {
        "use strict";

        var getTemplate = function (template, templateUrl) {
            var deferred = $q.defer();

            if(template) {
                deferred.resolve(template);
            } else if(templateUrl) {
                    var cachedTemplate = $templateCache.get(templateUrl);

                    if(cachedTemplate !== undefined) {
                      deferred.resolve(cachedTemplate);
                    }
                    else {
                        $http({method: 'GET', url: templateUrl, cache: true})
                            .then(function(result) {
                              $templateCache.put(templateUrl, result.data);
                              deferred.resolve(result.data);
                            })
                        .catch(function(error) {
                          deferred.reject(error);
                        });
                    }
            } else {
              deferred.reject("No template or templateUrl has been specified.");
            }
            return deferred.promise;
        };

        var service = {};

        service.getCurtain = function(options) {

            var deferredResponse = $q.defer();

            var controllerName = options.controller;
            if(!controllerName) {
              deferredResponse.reject("No controller has been specified.");
              return deferredResponse.promise;
            }

            if(options.controllerAs) {
              controllerName = controllerName + " as " + options.controllerAs;
            }

            getTemplate(options.template, options.templateUrl)
              .then(function(template) {

                var curtainScope = $rootScope.$new();

                var closeDeferred = $q.defer();
                var inputs = {
                  $scope: curtainScope,
                  close: function(result, delay) {
                    if(delay === undefined || delay === null) delay = 0;
                    $timeout(function () {
                      closeDeferred.resolve(result);
                    }, delay);
                  }
                };

                if(options.inputs) {
                  for(var inputName in options.inputs) {
                    inputs[inputName] = options.inputs[inputName];
                  }
                }

                var curtainElementTemplate = angular.element(template);

                var linkFn = $compile(curtainElementTemplate);
                var curtainElement = linkFn(curtainScope);
                inputs.$element = curtainElement;


                if (options.appendElement) {
                  options.appendElement.append(curtainElement);
                } else {
                  $document.find('body').append(curtainElement);
                }

                var curtain = {
                  scope: curtainScope,
                  element: curtainElement,
                  close: inputs.close
                };

                closeDeferred.promise.then(function(result) {
                  curtainScope.$destroy();
                  curtainElement.remove();
                });

                deferredResponse.resolve(curtain);
            })
            .catch(function(error) {
                deferredResponse.reject(error);
            });

            return deferredResponse.promise;
        };

        return service;

}]);  