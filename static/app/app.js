var app = angular.module('PowerHourApp', ['ngRoute', 'ngResource', 'ngCookies', 'ngMessages']);
 
app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);

app.config(['$resourceProvider', function($resourceProvider) {
	$resourceProvider.defaults.stripTrailingSlashes = false;
}]);

app.constant('Roles', {
	'GUEST'	: 'guest',
	'ADMIN' : 'admin',
	'USER' 	: 'user'
});

app.config(['$routeProvider', 'Roles', function ($routeProvider, Roles) {
	
	$routeProvider.when('/register', {
		controller: 'RegisterController',
		templateUrl: '/static/app/views/register.html',
		access: Roles.GUEST
	});

	$routeProvider.when('/welcome', {
		controller: 'WelcomeController',
		templateUrl: '/static/app/views/welcome.html',
		access: Roles.USER
	});

	$routeProvider.when('/playlist/:playlistId', {
		controller: 'PlaylistController',
		templateUrl: '/static/app/views/playlist.html',
		access: Roles.USER
	});

	$routeProvider.when('/profile', {
		controller: 'ProfileController',
		templateUrl: '/static/app/views/profile.html',
		access: Roles.USER
	});

	$routeProvider.when('/', {
		controller: 'MainController',
		templateUrl: '/static/app/views/test.html',
		access: Roles.GUEST
	});

	$routeProvider.when('/watch', {
		controller: 'PlayerController',
		templateUrl: '/static/app/views/loader.html',
		access: Roles.GUEST
	});

	$routeProvider.when('/login', {
		controller: 'LoginController',
		templateUrl: '/static/app/views/login.html',
		access: Roles.GUEST
	});

	$routeProvider.when('/create', {
		controller: 'CreateController',
		templateUrl: '/static/app/views/create.html',
		access: Roles.USER
	})

}]);

app.config(['$locationProvider', function($locationProvider) {
	$locationProvider.html5Mode({
		enabled: true,
		requireBase: false
	});
}]);

app.run(['$rootScope', '$location', 'Auth', 'Roles', function ($rootScope, $location, Auth, Roles) {
    $rootScope.$on("$routeChangeStart", function (event, next, current) {
        if (next.$$route.access !== Roles.GUEST && !Auth.isLoggedIn()) {
            $location.path('/');
        }
    });
}]);