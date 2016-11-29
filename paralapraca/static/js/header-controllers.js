(function(angular){
    'use strict';
    var app = angular.module('header.controllers', ['ngCookies']);

    app.controller('HeaderCtrl', [
        '$scope',
        '$rootScope',
        '$cookies',
        'CurrentUser',
        'Notification',
        'UnreadNotification',
        function ($scope, $rootScope, $cookies, CurrentUser, Notification, UnreadNotification) {

            $scope.user = CurrentUser;
            // FIXME Refactor this unsing CurrentUser service.
            $rootScope.is_main_nav_opened = $cookies.getObject('is_main_nav_opened');

            $scope.toggle_main_nav_display = function() {
                $rootScope.is_main_nav_opened = !$rootScope.is_main_nav_opened;
                $cookies.put('is_main_nav_opened', $rootScope.is_main_nav_opened);
            };

            // Start the header with the detailed notifications hidden
            $scope.show_notification = false;

            // Get the unread notifications count for the current user
            UnreadNotification.query(function(unread) {
                $scope.unread = unread[0];
                // if there are more than 9 notifications, reduce the number
                if($scope.unread.counter > 9){
                    $scope.unread.counter = "9+";
                }
            });

            $scope.toggle_notifications = function(){
                $scope.show_notification = !$scope.show_notification;
                UnreadNotification.update({id: $scope.unread.id, ignoreLoadingBar: true}, function(unread){
                    $scope.unread = unread;
                });
            }
        }
    ]);

})(window.angular);
