(function (angular) {
    'use strict';

    var module = angular.module('contracts.services', ['ngRoute', 'ngResource']);

    // TODO: insert Contract endpoint here
    module.factory('Contract', function($resource){
        // return $resource('/api/professor_message/:messageId', {}, {
        // });
    });

})(angular);
