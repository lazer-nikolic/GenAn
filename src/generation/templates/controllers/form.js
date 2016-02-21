{% import 'common.jinja' as common %}
(function () {
    'use strict';

    angular.module('{{concept.name}}')
        .controller('{{concept.name | title}}Controller', {{concept.name | title}}Controller);

    {{concept.name | title}}Controller.$inject = ['EventBus','{{concept.name | title}}Factory', '$filter', '$stateParams'];

    function {{concept.name | title}}Controller(EventBus, {{concept.name | title}}Factory, $filter, $stateParams) {

        var ctrl = this;
        ctrl.update = false;
        ctrl.oldObject = {};
        ctrl.currentObject = {};

        if ($stateParams.id != 'new') {
            {{concept.name | title}}Factory.getById($stateParams.id).then(function(success) {
                ctrl.currentObject = success;
                angular.copy(ctrl.currentObject, ctrl.oldObject);
                ctrl.update = true;
            });
        }

        ctrl.save = function () {
            if (ctrl.update) {
                {{concept.name | title}}Factory.update(ctrl.currentObject);
                angular.copy(ctrl.currentObject, ctrl.oldObject);
            } else {
                {{concept.name | title}}Factory.save(ctrl.currentObject);
                angular.copy(ctrl.currentObject, ctrl.oldObject);
            }
        }

        ctrl.restartUpdate = function () {
            angular.copy(ctrl.oldObject, ctrl.currentObject);
        }

        ctrl.cancel = function () {
            EventBus.emitEvent('GoToTableUser');
        }

        ctrl.remove = function () {
            {{concept.name | title}}Factory.remove(ctrl.currentObject.id);
            EventBus.emitEvent('GoToTableUser');
        }
    {for x in formInputs}
        {{x}}
        {}
    }
})();
