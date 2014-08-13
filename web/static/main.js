
var app = angular.module(
	'application', ['ngRoute', 'ngResource', 'ngCookies'],
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

app.controller('default', ['$scope', '$cookies', '$location',
  function ($scope, $cookies, $location) {
	  // debugger
  }]);

app.controller('index', ['$scope', '$http', '$location', '$cookieStore',
  function ($scope, $http, $location, $cookieStore) {
	  var url = '/level/';

	  $http.get(url).success(function(levels) {
		  $scope.levels_rows = [];
		  var i,j,temparray,chunk = 3;
		  for (i=0,j=levels.length; i<j; i+=chunk) {
			  var slice = levels.slice(i,i+chunk);
			  for (k=0; k<slice.length; k++) {
				  slice[k].result = $cookieStore.get(slice[k].key);
			  }
			  $scope.levels_rows.push(slice);
		  }
	  });

	  $scope.go = function(level) {
		  $location.path(level.key);
	  }

  }]);


app.controller('level', ['$scope', '$http', '$routeParams', '$location', '$cookieStore',
  function ($scope, $http, $routeParams, $location, $cookieStore) {
	  var url = '/level/' + $routeParams.hash + '/';

	  if (!$cookieStore.get($routeParams.hash)) {
		  $cookieStore.put($routeParams.hash, {
			  source: "",
			  score: 0,
			  length: 0,
		  })
	  }

	  $http.get(url).success(function(level) {
		  var cookie = $cookieStore.get($routeParams.hash);
		  $scope.source = cookie.source;

		  $scope.level = level;
		  $scope.score = 0;

		  var game = new Game(angular.element('#level'), level.content);

		  $scope.submit = function() {
			  cookie.source = $scope.source;
			  $cookieStore.put($routeParams.hash, cookie);

			  var data = {source: $scope.source};

			  $http.post(url, data).success(function(response) {
				  if (Object.keys(response.interpreted.error).length > 0) {
					  $scope.error = response.interpreted.error;
				  } else {
					  $scope.error = null;

					  game.reset();
					  game.walk(response.walk[0]).call(function() {
						  if (response.walk[2] > 0) {
							  $('.modal').modal({
								  backdrop: "static"
							  });
							  $scope.$apply(function () {
								  $scope.score = response.walk[2];
								  $scope.length = response.interpreted.length;

								  cookie.score = response.walk[2];
								  cookie.length = response.interpreted.length;
								  $cookieStore.put($routeParams.hash, cookie);
							  });
						  }
					  })
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
		  $scope.counter = $scope.source.replace(/\(|\)|\s|\n|\:|\,|\-|\+/g,'').length;
	  }

  }]);

