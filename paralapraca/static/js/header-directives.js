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
                    if(!$scope.notifications) {
                        $scope.notifications = Notification.query({limit_to: 10});
                    }
                }
            }
        }
    ]);

})(window.angular);
