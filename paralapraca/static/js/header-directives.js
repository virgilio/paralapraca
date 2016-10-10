(function(angular){
    'use strict';
    var app = angular.module('header.directives', []);

    app.directive('notifications', [
        'Notification',
        function(Notification){
            return {
                restrict: "E",
                templateUrl: "/static/templates/notifications.html",
                scope: {
                    'notifications': '=ngModel'
                },
                controller: function($scope) {
                    // Normalize all the diferent notification types for easy use in the template
                    $scope.parsed_notifications = [];
                    if(!$scope.notifications) {
                        $scope.notifications = Notification.query({limit_to: 10}, function(notifications){
                            for (var i = 0; i < notifications.length; i++) {
                                $scope.parsed_notifications[i] = {};
                                $scope.parsed_notifications[i].action = notifications[i].action;
                                $scope.parsed_notifications[i].date = notifications[i].date;
                                $scope.parsed_notifications[i].topic = notifications[i].topic;
                                $scope.parsed_notifications[i].forum = notifications[i].topic.forum;
                                switch (notifications[i].action) {
                                    case "new_topic":
                                        $scope.parsed_notifications[i].user = notifications[i].topic.author;
                                        break;
                                    case "new_comment":
                                        $scope.parsed_notifications[i].user = notifications[i].comment.author;
                                        break;
                                    case "new_reaction":
                                        $scope.parsed_notifications[i].user = notifications[i].topic_like.user;
                                        break;
                                    case "new_reaction_comment":
                                        $scope.parsed_notifications[i].user = notifications[i].comment_like.user;
                                        break;
                                    default:
                                        $scope.parsed_notifications[i] = notifications[i];
                                  }
                              }
                        });
                    }
                }
            }
        }
    ]);

})(window.angular);
