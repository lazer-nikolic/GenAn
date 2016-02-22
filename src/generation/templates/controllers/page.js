{% import 'common.jinja' as common %}
(function () {
    'use strict';

    angular.module('app')
        .controller('{{page.name | title}}Controller', {{page.name | title}}Controller);

    {{page.name | title}}Controller.$inject = ['EventBus',{% for factory in factories %}'{{factory | title}}Factory',{% endfor %} '$filter', '$stateParams'];

    function {{page.name | title}}Controller(EventBus, {% for factory in factories %}{{factory | title}}Factory,{% endfor %} $filter, $stateParams) {

        var ctrl = this;
         {% for factory in factories %}
             ctrl.{{factory}} = {};
             {{factory | title}}Factory.getAll().then(function (success) {
                ctrl.{{factory}} = success;
             });
         {% endfor %}
}


})();