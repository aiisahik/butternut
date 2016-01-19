'use strict';

angular.module('butternut.services')
    .factory('Profiles', ['$resource', function ($resource) {
        return $resource('/api/v1/profile/', {},
            {
                query: {isArray: false, method: 'GET'},
            }
        );
    }])
    .factory('Profile', ['$resource', function ($resource) {
        return $resource('/api/v1/profile/:id', {},
            {
                query: {isArray: false, method: 'GET'},
                update: {isArray: false, method: 'PUT'},
                create: {isArray: false, method: 'POST'},
                remove: {isArray: false, method: 'DELETE'}
            }
        );
    }])
    .factory('Matches', ['$resource', function ($resource) {
        return $resource('/api/v1/match/', {},
            {
                query: {isArray: false, method: 'GET'},
                create: {isArray: false, method: 'POST'},
            }
        );
    }])
    .factory('MatchCalculator', ['$resource', function ($resource) {
        return $resource('/calc/', {},
            {
                post: {isArray: false, method: 'POST'},
            }
        );
    }])

;