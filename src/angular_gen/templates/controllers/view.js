{% import 'common.jinja' as common %}
(function () {
    'use strict';

    angular.module('app')
        .controller('{{view.name | title}}Controller', {{view.name | title}}Controller);

    {{view.name | title}}Controller.$inject = ['EventBus', {% if main_factory %}'{{main_factory | title}}Factory',{% endif %}{% for factory in factories %}'{{factory | title}}Factory',{% endfor %} '$filter', '$stateParams'];

    function {{view.name | title}}Controller(EventBus, {% if main_factory %}{{main_factory | title}}Factory,{% endif %}{% for factory in factories %}{{factory | title}}Factory,{% endfor %} $filter, $stateParams) {

        var ctrl = this;
        {% if main_factory %}
        ctrl.{{main_factory}}_multiple  = {};
             ctrl.{{main_factory}} = {};
             {{main_factory | title}}Factory.getAll().then(function (success) {
                ctrl.{{main_factory}}_multiple  = success;
                if (ctrl.{{main_factory}}_multiple  && ctrl.{{main_factory}}_multiple.length>0) {
                 ctrl.{{main_factory}} = ctrl.{{main_factory}}_multiple[0];
             }
         });
         {% endif %}
         {% for factory in factories %}

             ctrl.{{factory}}_multiple  = {};
             ctrl.{{factory}} = {};
             {{factory | title}}Factory.{{factories[factory]}}().then(function (success) {
                ctrl.{{factory}}_multiple  = success;
                if (ctrl.{{factory}}_multiple  && ctrl.{{factory}}_multiple.length>0) {
                 ctrl.{{factory}} = ctrl.{{factory}}_multiple[0];
             }
             });
         {% endfor %}
}


})();