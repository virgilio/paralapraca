(function(angular){
    'use strict';
    var app = angular.module('header.controllers', []);

    app.controller('HeaderCtrl', [
        '$scope',
        'Notification',
        'CurrentUser',
        function ($scope, Notification, CurrentUser) {

            $scope.user = CurrentUser;
            $scope.show_notification = false;
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
                    filtered = 'gostou de um comentário no';
                    break;
            }
            return filtered;
        }
    });

    app.filter('dateFilter',function(){
        return function(dt) {
            var past = new Date(dt),
                now = new Date(),
                diff = now.getTime() - past.getTime(),
                labels = {
                    'ano': 31536000000,
                    'mês': 2592000000,
                    'semana': 604800000,
                    'dia': 86400000,
                    'hora': 3600000,
                    'minuto': 60000,
                    'segundo': 1000
                },
                time_int,
                filtered = [];
            angular.forEach(labels,function(val,time_unit){
                time_int = Math.floor(diff/val);
                if(diff>=val && time_int > 0) {
                    if(time_int > 1) {
                        if(time_unit == "mês") {
                            time_unit = 'meses';
                        }
                        else {
                            time_unit = time_unit+'s';
                        }
                    }
                    filtered.push(time_int+" "+time_unit);
                }
            });
            return filtered[0];
        }
    });

})(window.angular);
