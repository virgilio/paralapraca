(function(angular){
    'use strict';
    var app = angular.module('main-nav.controllers', []);

    app.controller('MainNavCtrl', [
        '$scope',
        function ($scope) {
            $scope.chat = {};

            // Listens to 'message' events triggered by the Rocket Chat iframe
            window.addEventListener('message', function(e) {
                var counter;
                if(e.data.eventName === 'unread-changed'){
                    counter = e.data.data;
                    if(counter > 9)
                        // if there are more than 9 notifications, reduce the number
                        $scope.chat.notifications = "9+";
                    else if(e.data.data === "")
                        // If the data value is empty, then it must be set to zero
                        $scope.chat.notifications = 0;
                    else
                        // Otherwise, the number must be used as is
                        $scope.chat.notifications = e.data.data;

                    // Ensures that the template is updated as soon as possible
                    $scope.$apply();
                }
            });
        }
    ]);

})(window.angular);
