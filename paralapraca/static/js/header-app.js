(function(angular){
    'use strict';

    var app = angular.module('header', [
        'header.services',
        'header.controllers',
        'header.directives',
        'header.filters',
        'main-nav',
        'main-nav.controllers',
        'discussion.services',
        'djangular',
        'gettext',
        'ngAnimate',
        'angular-loading-bar',
        'angular-click-outside',
        'ui.bootstrap',
    ]);

    app.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
        cfpLoadingBarProvider.spinnerTemplate = '<div class="loading-background"></div><div class="loading-spinner fa fa-spinner fa-pulse fa-4x"></div>';
    }]);

})(angular);
