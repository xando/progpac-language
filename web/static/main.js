
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


app.controller('level', ['$scope', '$http', '$routeParams', '$location',
  function ($scope, $http, $routeParams, $location) {
	  var url = '/level/' + $routeParams.hash + '/';

	  $http.get(url).success(function(level) {
		  $scope.level = level;

		  var game = new Game(angular.element('#level'), level.content);

		  $scope.submit = function() {
			  var data = {source: $scope.source};

			  $http.post(url, data).success(function(response) {
				  if (Object.keys(response.interpreted.error).length > 0) {
					  $scope.error = response.interpreted.error;
				  } else {
					  $scope.error = null;

					  game.reset();
					  game.walk(response.walk[0]).call(function() {

						  $('.modal').modal({
							  backdrop: "static"
						  });

					  })

					  var is_solved = response.walk[2];
					  if (is_solved) {

					  }

				  }
			  });
		  }

		  $scope.go_restart = function() {
			  $('.modal').modal('hide');
			  game.reset();
		  }

		  $scope.go_continue = function() {
			  $('.modal').modal('hide');
			  // Modal bug
			  $('.modal-backdrop').remove();
			  $location.path('/');
		  }
	  });

	  $scope.counter = 0;
	  $scope.update_counter = function() {
		  $scope.counter = $scope.source.replace(/\s|\:|\(|\)|\,/g,'').length;
	  }

  }]);

