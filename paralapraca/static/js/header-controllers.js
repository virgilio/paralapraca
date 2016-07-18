(function(angular){
    'use strict';
    var app = angular.module('header.controllers', []);

    app.controller('HeaderCtrl', ['$scope',
        function ($scope) {
            $scope.show_notification = false;
        }
    ]);

})(window.angular);
