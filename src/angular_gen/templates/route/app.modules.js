{% import 'common.jinja' as common %}
(function () {
    'use strict';

    angular
        .module('app', [
            'ngAnimate', 'ngTouch', 'ngSanitize', 'ngLocale',
            'ui.router', 'ui.bootstrap',
            'app.config',
            'app.translation',
            'app.eventbus',
            'app.layout',
            'app.about-us',
            'app.api'
        ]);
})();