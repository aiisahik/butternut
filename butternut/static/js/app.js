'use strict';

angular.module('butternut.public', [
    'ngResource', 
	'ui.bootstrap', 
	'butternut.services', 
	'butternut.controllers', 
	'ui.router',
  	])

    .config(['$httpProvider', '$resourceProvider', '$sceDelegateProvider', '$stateProvider', '$urlRouterProvider', 
    	function ($httpProvider, $resourceProvider, $sceDelegateProvider, $stateProvider, $urlRouterProvider) {
        // $httpProvider.interceptors.push('authInterceptor');
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }])
;