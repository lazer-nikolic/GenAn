{% import 'common.jinja' as common %}
(function() {
    'use strict';

    angular
        .module('app')
        .config(routes)
        .run(run);

    routes.$inject = ['$stateProvider', '$urlRouterProvider', '$httpProvider','newRoutes'];
    var $stateProviderRef;

    function routes($stateProvider, $urlRouterProvider, $httpProvider, newRoutes) {

            for (var stateName in newRoutes){
                var state = newRoutes[stateName];
                $stateProvider.state(stateName, state);
            }

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
                        {% if routes[route].overriden %}
                            controller: 'User{{routes[route].controller|title}}Controller',
                        {% else %}
                            controller: '{{routes[route].controller|title}}Controller',
                        {% endif %}

                        controllerAs: 'ctrl_page'
                    }
                    {% set all_routes = routes[route]|sub_routes%}
                    {% for sub_route in  all_routes %}
                    ,
                    '{{sub_route.name}}@{{route}}': {
                        templateUrl: '{{sub_route.template}}',
                        {% if sub_route.overriden %}
                            controller: 'User{{sub_route.controller|title}}Controller',
                        {% else %}
                            controller: '{{sub_route.controller|title}}Controller',
                        {% endif %}
                        controllerAs: 'ctrl'
                    }
                    {% endfor %}
                }
            })
    {% endfor %};

            {% if customIndexRoute %}
                $urlRouterProvider.otherwise('{{ customIndexRoute.path }}');
            {% else %}
                $urlRouterProvider.otherwise('/index');
            {% endif %}
        }

    run.$inject = ['Routing'];
    function run(Routing) {
    }
    })();
