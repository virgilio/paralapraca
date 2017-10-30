(function(angular){
    'use strict';
    var app = angular.module('contracts.controllers', []);

    app.controller('ContractsCtrl', ['$scope', 'Contracts',
        function ($scope, Contracts) {
            $scope.contracts = Contracts.query();
        }
    ]);

    app.controller('ContractDetailsCtrl', ['$scope', '$routeParams', 'Contracts',
        function ($scope, $routeParams, Contracts) {
            $scope.contract_id = $routeParams.contractId;
            $scope.contract = Contracts.get({id: $scope.contract_id});
        }
    ]);

    app.controller('NewContractCtrl', ['$scope', 'Contracts',
        function ($scope, Contracts) {
            $scope.editing_mode = false;
        }
    ]);

    app.controller('EditContractCtrl', ['$scope', '$routeParams', 'Contracts',
        function ($scope, $routeParams, Contracts) {
            $scope.editing_mode = true;
            $scope.contract_id = $routeParams.contractId;
            $scope.contract = Contracts.get({id: $scope.contract_id});
        }
    ]);


})(window.angular);
