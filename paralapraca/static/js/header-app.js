(function(angular){
    'use strict';

    var app = angular.module('header', [
        'header.controllers',
        'header.directives',
        'header.filters',
        'discussion.services',
        'djangular',
        'gettext',
        'ngAnimate',
        'angular-loading-bar',
    ]);

    app.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
        cfpLoadingBarProvider.spinnerTemplate = '<div class="" style="top: 0; bottom: 0; left: 0; right: 0; position: fixed; background: rgba(255,255,255,0.6);"></div><div class="fa fa-spinner"></div>';
    }]);

})(angular);
