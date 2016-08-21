{% import 'common.jinja' as common %}
(function () {
    'use strict';

    angular.module('app')
        .controller('{{page.name | title}}Controller', {{page.name | title}}Controller);

    {{page.name | title}}Controller.$inject = ['EventBus',{% for factory in factories %}'{{factory | title}}Factory',{% endfor %} '$filter', '$stateParams'];

    function {{page.name | title}}Controller(EventBus, {% for factory in factories %}{{factory | title}}Factory,{% endfor %} $filter, $stateParams) {

        var ctrl_page = this;
         {% for factory in factories %}
             ctrl_page.{{factory}}_multiple = {};
             ctrl_page.{{factory}} = {};
             {{factory | title}}Factory.{{factories[factory]}}().then(function (success) {
                ctrl_page.{{factory}}_multiple  = success;
                if (ctrl_page.{{factory}}_multiple && ctrl_page.{{factory}}_multiple.length > 0) {
                    /* todo: correct usage of parameters */
                    for(var i = 0;  i < ctrl_page.{{factory}}_multiple.length; i++) {
                        var {{factory}}_single = ctrl_page.{{factory}}_multiple[i];
                        if({{factory}}_single._id == $stateParams.id) {
                            ctrl_page.{{factory}} = {{factory}}_single;
                        }
                    }
                }
             });
         {% endfor %}
}


})();