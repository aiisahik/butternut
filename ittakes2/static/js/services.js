angular.module('ittakes2.services', [])
	.factory('DataService', ['$q', 'Profiles', 'Profile', 'Matches', function ($q, Profiles, Profile, Matches) {
		var service = {};
		service.profiles_defer = $q.defer();

		service.get_profiles = function(force_refresh){
				if (force_refresh){
					service.profiles_defer = $q.defer();
				}
				if (!service.profiles || force_refresh){

	        		Profiles.query().$promise.then(function(result){
	        			if (result && result.objects){
	        				service.profiles = result.objects;
	        			}
	        			service.profiles_defer.resolve(service.profiles);
	        		})
				} else {
					service.profiles_defer.resolve(service.profiles);
				}
				return service.profiles_defer
        }
		service.get_matches = function(force_refresh){
				var defer = $q.defer();
				if (!service.matches || force_refresh){
					service.profiles_defer.promise.then(function(profiles_result){
						var profiles_dict = {}
						_.each(profiles_result,function(profile){
							profiles_dict[profile.user_id] = profile;
						});
						console.log('profiles dict', profiles_dict);
		        		Matches.query().$promise.then(function(result){
		        			if (result && result.objects){
		        				var matches = result.objects;
		        				_.each(matches, function(match){
		        					match.winner = profiles_dict[match.winner_id];
		        					match.loser = profiles_dict[match.loser_id];
		        				})
		        				service.matches = matches;
		        			}
		        			defer.resolve(service.matches);
		        		})
					})
				} else {
					defer.resolve(service.matches);
				}
				return defer
        }
		return service;
	}])
	// .factory('MatchService', ['$q', 'Matches', function ($q, Matches) {
	// 	var service = {};
	// }])
;