'use strict';

angular.module('ittakes2.public', [
    'ngResource', 
	'ui.bootstrap', 
	'ittakes2.services', 
	'ittakes2.controllers', 
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