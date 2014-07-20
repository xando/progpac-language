
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
			.when('/level/:id', {
				templateUrl: '/templates/level.html',
				controller: 'level'
			});

	});


app.controller('index', ['$scope', '$http',
  function ($scope, $http) {

  }]);


app.controller('level', ['$scope', '$http',
  function ($scope, $http) {

	  $scope.submit = function() {
		  var data = {source: $scope.source};

		  $http.post('/validate/', data).success(function(response) {
			  $scope.error = response.error;
		  });
	  }

  }]);

