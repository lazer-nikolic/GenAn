 {% import 'common.jinja' as common %}
 ctrl.{{name}}Datepicker = function ($event) {
    $event.preventDefault();
    $event.stopPropagation();
    ctrl.{{name}}Opened = true;
};