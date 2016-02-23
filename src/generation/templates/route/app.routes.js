{% import 'common.jinja' as common %}
(function() {
    'use strict';

    angular
        .module('app')
        .config(routes)
        .run(run);

    routes.$inject = ['$stateProvider', '$urlRouterProvider', '$httpProvider'];

    function routes($stateProvider, $urlRouterProvider, $httpProvider) {
        $stateProvider
            .state('index', {
                url: '/index',
                templateUrl: 'app/components/index.html',
                controller: 'IndexController'
            })
            .state('about', {
                url: '/about',
                templateUrl: 'app/components/about/about.us.html',
                controller: 'AboutUsController',
                controllerAs: 'ctrl'
            })
        {%for route in routes %}
         .state('{{route}}', {
                url: '{{routes[route].path}}',
                views: {
                    'center': {
                        templateUrl: '{{routes[route].template}}',
                        controller: '{{routes[route].controller|title}}Controller',
                        controllerAs: 'ctrl'
                    }

                    {% for sub_route in routes[route].sub_routes %}
                    ,
                    '{{sub_route.name}}': {
                        templateUrl: '{{sub_route.template}}',
                        controller: '{{sub_route.controller|title}}Controller',
                        controllerAs: 'ctrl'
                    }
                    {% endfor %}
                }
            })
            {% endfor %};

            $urlRouterProvider.otherwise('/index');
        }

    run.$inject = ['Routing'];
    function run(Routing) {
    }
    })();
