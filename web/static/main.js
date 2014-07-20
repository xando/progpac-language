
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
		  var data = {code: $scope.code};

		  $http.post('/validate/', data).success(function(response) {
			  debugger
		  });

	  }
  }]);


// function index($scope, $routeParams, $location) {
// }

// .factory('Person', ['$resource', function($resource) {
// 	return $resource('/person/:id', {id:'@id'}, {
// 		'update': {method:'PUT'}
// 	});
// }]);


	// $scope.people = Person.query();
	// $scope.test = "Seba";

	// $scope.submit = function() {

	// 	Person.save({
	// 		first_name: $scope.firstname,
	// 		last_name: $scope.lastname,
	// 	}, function() {
	// 		// success
	// 	}, function(response) {
	// 		$scope.error = response.data;
	// 	})

	// };
