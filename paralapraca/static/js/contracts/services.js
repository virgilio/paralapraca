(function (angular) {
    'use strict';

    var app = angular.module('contracts.services', ['ngRoute', 'ngResource']);

    app.factory('Contracts', function($resource){
        return $resource('/paralapraca/api/contract/:id',
            {'id': '@id'});
    });

})(angular);
