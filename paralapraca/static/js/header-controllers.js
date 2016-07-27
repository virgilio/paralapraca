(function(angular){
    'use strict';
    var app = angular.module('header.controllers', []);

    app.controller('HeaderCtrl', ['$scope','Notification',
        function ($scope, Notification) {
            $scope.show_notification = true;
            $scope.notifications_loaded = false;
            $scope.notifications = Notification.query(function(res){
                $scope.notifications_loaded = true;
            });
        }
    ]);

    app.filter('actionFilter',function(){
        return function(txt) { // [ação no] tópico tal
            var filtered;
            switch(txt) {
                case 'new_comment':
                    filtered = 'comentou no';
                    break;
                case 'new_topic':
                    filtered = 'criou o';
                    break;
                case 'new_reaction':
                    filtered = 'gostou do';
                    break;
                case 'new_reaction_comment':
                    filtered = 'gostou do comentário no';
                    break;
            }
            return filtered;
        }
    });

})(window.angular);
