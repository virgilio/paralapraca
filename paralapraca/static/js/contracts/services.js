(function (angular) {
    'use strict';

    var app = angular.module('contracts.services', ['ngRoute', 'ngResource']);

    app.factory('Contracts', ['$resource', function($resource){
        return $resource('/paralapraca/api/contract/:id',
            {'id': '@id'});
    }]);

    app.factory('Courses', ['$resource', function($resource){
        return $resource('/api/course/:id',
            {'id': '@id'});
    }]);

})(angular);
