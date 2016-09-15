(function(angular){
    'use strict';
    var app = angular.module('header.controllers', ['ngCookies']);

    app.controller('HeaderCtrl', [
        '$scope',
        '$rootScope',
        '$cookies',
        'CurrentUser',
        'Notification',
        function ($scope, $rootScope, $cookies, CurrentUser, Notification) {

            $scope.user = CurrentUser;
            // FIXME Refactor this unsing CurrentUser service.
            $rootScope.is_main_nav_opened = $cookies.getObject('is_main_nav_opened');

            $scope.toggle_main_nav_display = function() {
                $rootScope.is_main_nav_opened = !$rootScope.is_main_nav_opened;
                $cookies.put('is_main_nav_opened', $rootScope.is_main_nav_opened);
            };

            $scope.show_notification = false;
        }
    ]);

})(window.angular);
