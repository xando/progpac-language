
var app = angular.module(
	'application', ['ngRoute', 'ngResource'],
	function($routeProvider, $resourceProvider, $httpProvider) {

		$resourceProvider.defaults.stripTrailingSlashes = false;
		$httpProvider.defaults.xsrfCookieName = 'csrftoken';
		$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

		$routeProvider
			.when('/', {
				templateUrl: '/static/templates/index.html',
				controller: 'index'
			})
			.when('/:hash', {
				templateUrl: '/static/templates/level.html',
				controller: 'level'
			});

	});


app.controller('index', ['$scope', '$http', '$location',
  function ($scope, $http, $location) {
	  var url = '/level/';

	  $http.get(url).success(function(levels) {
		  $scope.levels_rows = [];
		  var i,j,temparray,chunk = 3;
		  for (i=0,j=levels.length; i<j; i+=chunk) {
			  $scope.levels_rows.push(levels.slice(i,i+chunk))
		  }
	  });

	  $scope.go = function(level) {
		  $location.path(level.key);
	  }

  }]);


app.controller('level', ['$scope', '$http', '$routeParams',
  function ($scope, $http, $routeParams) {

	  var url = '/level/' + $routeParams.hash + '/';

	  $http.get(url).success(function(level) {
		  $scope.level = level;
		  var game = new Game(angular.element('.render'), level.content);

		  $scope.submit = function() {
			  var data = {source: $scope.source};

			  $http.post(url, data).success(function(response) {
				  if (Object.keys(response.interpreted.error).length > 0) {
					  $scope.error = response.interpreted.error;
				  } else {
					  game.reset();
					  $scope.error = null;
					  game.walk(response.walk[0]);
				  }
			  });
		  }

	  });


  }]);

