(function(angular){
    'use strict';

    var app = angular.module('header', [
        'header.controllers',
        'header.directives',
        'header.filters',
        'discussion.services',
        'djangular',
    ]);
})(angular);
