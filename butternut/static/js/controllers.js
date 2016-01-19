angular.module('butternut.controllers', [])

    .controller('homeController', ['$scope', 'DataService', function ($scope, DataService) {
        var vm = this; 
        	DataService.get_profiles();

    }])
    .controller('rankingsController', ['$scope', 'DataService', 'MatchCalculator', 
    	function ($scope, DataService, MatchCalculator) {
        var vm = this;
        	vm.loading = false;
        	vm.init = function(){
        		vm.loading = true;
	        	DataService.profiles_defer.promise.then(function(result){
	        		vm.loading = false;
	        		vm.profiles = result;
	        	});
        	}
        	vm.calc = function(){
        		vm.loading = true;
        		MatchCalculator.post({calc: 'all'}).$promise.then(function(result){
        			if (result.success){
        				DataService.get_profiles(true).promise.then(function(result){
        					vm.loading = false;
			        		vm.profiles = result;
			        	});
        			} else {
        				vm.loading = false;
        			}

        		})
        	}
        	vm.init();
        	
    }])
    .controller('matchesController', ['$scope', 'DataService', 'MatchCalculator', 
    	function ($scope, DataService, MatchCalculator) {
        var vm = this;
        	vm.loading = false;
        	vm.init = function(){
        		vm.loading = true;
	        	DataService.get_matches().promise.then(function(result){
	        		vm.loading = false;
	        		vm.matches = result;
	        		console.log(vm.matches)
	        	});
        	}
        	vm.init();
    }])
    .controller('newMatchController', ['$scope', 'DataService', 'Matches',
    	function ($scope, DataService, Matches) {
        var vm = this;
        	vm.loading = false;
        	vm.winner_profiles = [];
        	vm.loser_profiles = [];
        	vm.form_data = {winner_score: 21};
        	vm.init = function(){
        		vm.loading = true;
        		DataService.profiles_defer.promise.then(function(result){
	        		vm.loading = false;
        			var profiles = result;
        			vm.winner_profiles = angular.copy(profiles);
        			vm.loser_profiles = angular.copy(profiles);
	        	});
        	}
        	vm.update_profiles = function(){
        		if (vm.form_data.loser){
	        		vm.winner_profiles = _.filter(vm.winner_profiles, function( profile ){
	        			return (profile.user_id !== vm.form_data.loser.user_id);
	        		})
	        	}
	        	if (vm.form_data.winner){
	        		vm.loser_profiles = _.filter(vm.loser_profiles, function( profile ){
	        			return (profile.user_id !== vm.form_data.winner.user_id);
	        		})
	        	}
        	}
        	vm.reset = function(){
        		vm.new_match = null;
        		vm.form_data = {winner_score: 21};
        	}
        	vm.submit = function($form){
        		if ($form.$valid){
        			vm.loading = true;
        			Matches.create(vm.form_data).$promise.then(function(result){
        				vm.loading = false;
        				vm.new_match = result;
        			})
        		}
        	}
        	vm.init();
    }])
;
