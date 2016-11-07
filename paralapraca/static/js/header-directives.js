(function(angular) {
    'use strict';
    var app = angular.module('header.directives', []);

    app.directive('notifications', [
        '$q',
        'Notification',
        'AnswerNotification',
        function($q, Notification, AnswerNotification) {
            return {
                restrict: "E",
                templateUrl: "/static/templates/notifications.html",
                scope: {
                    'notifications': '=ngModel'
                },
                controller: function($scope) {
                    // Normalize all the diferent notification types for easy use in the template
                    $scope.parsed_notifications = [];
                    if (!$scope.notifications) {
                        // Both notification sources must resolve before $scope.parsed_notifications can be created
                        $q.all({
                                discussion: Notification.query({limit_to: 10}).$promise,
                                answer: AnswerNotification.query({limit_to: 10}).$promise
                            })
                            .then(
                                function(notifications) {
                                    // Parse notifications from discussion app
                                    for (var i = 0; i < notifications.discussion.length; i++) {
                                        $scope.parsed_notifications[i] = {};
                                        $scope.parsed_notifications[i].action = notifications.discussion[i].action;
                                        $scope.parsed_notifications[i].date = notifications.discussion[i].date;
                                        $scope.parsed_notifications[i].topic = notifications.discussion[i].topic;
                                        $scope.parsed_notifications[i].forum = notifications.discussion[i].topic.forum;
                                        $scope.parsed_notifications[i].is_read = notifications.discussion[i].is_read;
                                        switch (notifications.discussion[i].action) {
                                            case "new_topic":
                                                $scope.parsed_notifications[i].user = notifications.discussion[i].topic.author;
                                                break;
                                            case "new_comment":
                                                $scope.parsed_notifications[i].user = notifications.discussion[i].comment.author;
                                                break;
                                            case "new_reaction":
                                                $scope.parsed_notifications[i].user = notifications.discussion[i].topic_like.user;
                                                break;
                                            case "new_reaction_comment":
                                                $scope.parsed_notifications[i].user = notifications.discussion[i].comment_like.user;
                                                break;
                                            default:
                                                $scope.parsed_notifications[i] = notifications.discussion[i];
                                        }
                                    }
                                    // Include notifications from activities answers (if any)
                                    $scope.parsed_notifications = $scope.parsed_notifications.concat(notifications.answer);

                                    // Notifications are ready to be shown, so the template must be alerted
                                    $scope.notifications_ready = true;

                                });

                    }
                }
            };
        }
    ]);

})(window.angular);
