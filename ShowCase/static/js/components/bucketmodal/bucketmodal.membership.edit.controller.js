angular.module('module.bucketmodal')
.controller('bucketmodalEditMembershipController', ['$scope',
    'bucketModel',
    'bucketmodalService',
    'close',
    'membership',
    'bucket',
    'progress',
    'alert',
    function ($scope, bucketModel, bucketmodalService, close, membership, bucket, progress, alert) {
        var addingCount = 0;

        $scope.bucket = bucket;
        $scope.membership = membership;
        $scope.updatingMembership = false;

        $scope.updateBucketMembership = function () {
            $scope.updatingMembership = true;

            bucketModel.updateBucketMembership(bucket.id,
                membership.composition.id,
                $scope.membership)
            .then(function (membership) {
                $scope.close();
            }, function () {
                $scope.updatingMembership = false;
                alert.showAlert('Unable to update membershipinformation to this series');
            })
        };

        $scope.holdClick = function (event) {
            event.stopPropagation();
        }

        $scope.close = function () {
            close();
        };
    }
]);