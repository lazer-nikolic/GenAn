{% import 'common.jinja' as common %}
(function () {
    'use strict';

    angular.module('app')
        .controller('{{name | title}}_formController', {{name | title}}formController);

    {{name | title}}formController.$inject = ['EventBus','{{name | title}}Factory',
    {%- for m in meta %} '{{m.name | title}}Factory',{% endfor %} '$filter', '$stateParams'];

    function {{name | title}}formController(EventBus, {{name | title}}Factory,
    {%- for m in meta %} {{m.name | title}}Factory,{% endfor %} $filter, $stateParams) {

        var ctrl = this;
        ctrl.update = false;
        ctrl.oldObject = {};
        ctrl.{{name}} = {};

        /*** meta init ***/

        {% for m in meta %}
            ctrl.meta_{{ m.name }} = {};
        {% endfor %}

        {% for m in meta %}
            ctrl.getAll_meta_{{ m.name }} = function() {
                {{m.name | title}}Factory.getAll().then(function(success) {
                    ctrl.meta_{{ m.name }} = success;
                });
            }
        {% endfor %}

        {% for m in meta %}
            ctrl.getAll_meta_{{ m.name }}();
        {% endfor %}

        /*******/

        if ($stateParams.id  !== undefined && $stateParams.id != "") {
            {{name | title}}Factory.getById($stateParams.id).then(function(success) {
                ctrl.{{name}} = success;
                angular.copy(ctrl.{{name}}, ctrl.oldObject);
                ctrl.update = true;
            });
        }

        ctrl.save = function () {
            if (ctrl.update) {
                {{name | title}}Factory.update(ctrl.{{name}});
                angular.copy(ctrl.{{name}}, ctrl.oldObject);
            } else {
                {{name | title}}Factory.create(ctrl.{{name}});
                angular.copy(ctrl.{{name}}, ctrl.oldObject);
            }
        }

        ctrl.resetUpdate = function () {
            angular.copy(ctrl.oldObject, ctrl.{{name}});
        }

        ctrl.cancel = function () {
            EventBus.emitEvent('GoToTableUser');
        }

        ctrl.remove = function () {
            {{name | title}}Factory.remove(ctrl.{{name}}.id);
            EventBus.emitEvent('GoToTableUser');
        }
    {%for x in formInputs %}
        {{x}}
   {% endfor %}
}}
)();
