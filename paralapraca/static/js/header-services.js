(function(angular){
    'use strict';
    var app = angular.module('header.services', ['ngResource']);

    app.factory('UnreadNotification', ['$resource', function($resource){
        return $resource('/paralapraca/api/unread-notification/:id',
            {'id' : '@id'},
            {'update': {'method': 'PUT', 'ignoreLoadingBar': true} });
    }]);

})(window.angular);
