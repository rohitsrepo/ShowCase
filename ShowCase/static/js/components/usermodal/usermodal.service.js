angular.module('module.usermodal')
.factory('usermodalService', ['$q',
    'modalService',
    'followService',
    'userModel',
    'compositionModel',
    'admirationModel',
    'bookService',
    function ($q, modalService, followService, userModel, compositionModel, admirationModel, bookService) {
    var service = {};

    var showuserModal = function (inputData) {
        return modalService.showModal({
            'templateUrl': '/static/js/components/usermodal/usermodal.tpl.html',
            'controller': 'usermodalController',
            'inputs' : {
                'inputData': inputData
            }
        }).then(function (modal) {
            return modal.close;
        });
    };

    service.showBookMarkers = function (art) {
        var inputData = {
            'noUserInfo': 'No bookmarkers yet',
            'noUserMessage': 'Do you find this work worth keeping?',
            'noUserActionResult': 'bookmarked',
            'noUserActionMessage': 'BOOKMARK',
            'noUserAction': function () {
                return bookService.bookmarkArt(art);
            },
            'usersFetcher': function () {
                return compositionModel.getBookMarkers(art.id);
            }

        };

        return showuserModal(inputData);
    };

    service.showFollowers = function (user) {
        var inputData = {
            'noUserInfo': 'User is not followed by anyone yet',
            'noUserMessage': 'Is there a hint of matching taste?',
            'noUserActionResult': 'followed',
            'noUserActionMessage': 'FOLLOW',
            'noUserAction': function () {
                return followService.follow(user);
            },
            'usersFetcher': function () {
                return userModel.getFollowers(user.id);
            }

        };

        return showuserModal(inputData);
    };

    service.showFollows = function (user) {
        var inputData = {
            'noUserInfo': 'User is not following anyone yet',
            'noUserMessage': '',
            'noUserActionResult': '',
            'noUserActionMessage': '',
            'noUserAction': function () {},
            'usersFetcher': function () {
                return userModel.getFollows(user.id);
            }

        };

        return showuserModal(inputData);
    };

    var showAdmirers = function (object_id, content_type) {
        var inputData = {
            'noUserInfo': 'Artwork has not been admired by anyone yet',
            'noUserMessage': 'Does this work evoke a thought...good or bad?',
            'noUserActionResult': 'admired',
            'noUserActionMessage': 'ADMIRE',
            'noUserAction': function () {
                return admirationModel.admire(object_id, content_type);
            },
            'usersFetcher': function () {
                var deferred = $q.defer();
                return admirationModel.getAdmirations(object_id, content_type);
            }

        };

        return showuserModal(inputData);
    };

    service.showArtAdmirers = function (art) {
        return showAdmirers(art.id, admirationModel.TypeArt);
    };

    service.showBucketAdmirers = function (bucket) {
        return showAdmirers(bucket.id, admirationModel.TypeBucket);
    };

    return service;
}]);