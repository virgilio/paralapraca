(function(angular){
    'use strict';
    var app = angular.module('main-nav.controllers', []);

    app.controller('MainNavCtrl', [
        '$scope', 'Message',
        function ($scope, Message) {

            // Count unread messages for display in the main navigation
            $scope.messages_unread_count = 0;
            Message.query({}, function(message){
                for (var i = 0; i < message.length; i++) {
                    if (message[i].is_read === false)
                        $scope.messages_unread_count++;
                }
            })

            // Listens to 'message' events triggered by the Rocket Chat iframe
            $scope.chat = {};
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
