(function(angular){
    'use strict';
    var app = angular.module('main-nav.controllers', []);

    app.controller('MainNavCtrl', [
        '$scope',
        function ($scope) {

            $scope.chat = {};
            window.addEventListener('message', function(e) {
                if(e.data.eventName === 'unread-changed'){
                    if(e.data.data !== "")
                        $scope.chat.notifications = e.data.data;
                    else
                        $scope.chat.notifications = 0;
                console.log($scope.chat.notifications);
                }
            });
        }
    ]);

})(window.angular);
