(function(angular){
    'use strict';
    var app = angular.module('contracts.controllers', []);

    app.controller('ContractsCtrl', ['$scope', 'Contracts',
        function ($scope, Contracts) {
            $scope.contracts = Contracts.query();
        }
    ]);

    app.controller('ContractDetailsCtrl', ['$scope', 'Contracts',
        function ($scope, Contracts) {

        }
    ]);

    app.controller('NewContractCtrl', ['$scope', 'Contracts',
        function ($scope, Contracts) {

        }
    ]);

    app.controller('EditContractCtrl', ['$scope', 'Contracts',
        function ($scope, Contracts) {

        }
    ]);


})(window.angular);
