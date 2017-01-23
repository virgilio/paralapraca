(function (angular) {
    'use strict';

    var module = angular.module('main-nav.services', ['ngRoute', 'ngResource']);

    module.factory('Message', function($resource){
            return $resource('/api/professor_message/:messageId', {}, {
            });
    });

})(angular);
