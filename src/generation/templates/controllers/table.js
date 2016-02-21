{% import 'common.jinja' as common %}
(function () {
    'use strict';

    angular.module('{{data[0].object.name}}')
        .controller('{{data[0].object.name | title}}Controller', {{data[0].object.name | title}}Controller);

    {{data[0].object.name | title}}Controller.$inject = ['EventBus', '{{data[0].object.name | title}}Factory', '$filter'];

    function {{data[0].object.name | title}}Controller(EventBus, {{data[0].object.name | title}}Factory, $filter) {

        var ctrl = this;
        ctrl.update = false;
        ctrl.selected = null;
        ctrl.users = {};
        {{data[0].object.name | title}}Factory.getAll().then(function(success) {
            ctrl.users = success;
        });

        ctrl.setSelected = function (selected) {
            ctrl.selected = selected;
        };

        ctrl.update = function (id) {
            EventBus.emitEvent('GoToFormUser', {
                id: id
            });
        }

        ctrl.remove = function (id) {
            {{data[0].object.name | title}}Factory.remove(id);
            EventBus.emitEvent('GoTo{{data[0].object.name | title}}');
        }
    }
})();
