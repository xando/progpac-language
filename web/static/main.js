
var app = angular.module(
	'application', ['ngRoute', 'ngResource'],
	function($routeProvider, $resourceProvider, $httpProvider) {

		$resourceProvider.defaults.stripTrailingSlashes = false;
		$httpProvider.defaults.xsrfCookieName = 'csrftoken';
		$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

		$routeProvider
			.when('/', {
				templateUrl: '/templates/index.html',
				controller: 'index'
			})
			.when('/:hash', {
				templateUrl: '/templates/level.html',
				controller: 'level'
			});

	});


app.controller('index', ['$scope', '$http',
  function ($scope, $http) {

  }]);


app.controller('level', ['$scope', '$http', '$routeParams',
  function ($scope, $http, $routeParams) {

	  var url = '/level/' + $routeParams.hash;

	  $http.get(url).success(function(level) {
		  $scope.level = level;
		  var game = new Game(angular.element('.render'), level.content);

		  $scope.submit = function() {
			  game.reset();
			  var data = {source: $scope.source};

			  $http.post(url + '/validate/', data).success(function(response) {
				  game.walk(response[0]);
				  // $scope.error = response.error;
			  });
		  }

	  });


  }]);

