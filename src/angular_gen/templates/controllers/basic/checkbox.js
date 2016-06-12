    {% import 'common.jinja' as common %}
    ctrl.selected{{name}} = {};
    ctrl.getSelectedItemsFor{{name}} = function() {
        ctrl.{{name}} = [];
        for (name in ctrl.selected{{name}}) {
            if (ctrl.selected{{name}}[name]) {
                ctrl.{{name}}.push(name);
            }
        }
    }
