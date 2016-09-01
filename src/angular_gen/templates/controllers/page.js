{% import 'common.jinja' as common %}
(function () {
    'use strict';

    angular.module('app')
        .controller('{{page.name | title}}Controller', {{page.name | title}}Controller);

    {{page.name | title}}Controller.$inject = ['EventBus', {% if main_factory %}'{{main_factory | title}}Factory',{% endif %}{% for factory in factories %} '{{factory | title}}Factory',{% endfor %} '$filter', '$stateParams'];

    /*
    We use page controller to access single entities because, when we access single item,
    we pass url parameters like ID which are accessible only through page controller.
    */
    function {{page.name | title}}Controller(EventBus, {% if main_factory %}{{main_factory | title}}Factory,{% endif %}{% for factory in factories %} {{factory | title}}Factory,{% endfor %} $filter, $stateParams) {

        var ctrl_page = this;
        {% if main_factory %}
         ctrl_page.{{main_factory}} = {};

         {{main_factory | title}}Factory.getById($stateParams.id).then(function (success) {
            ctrl_page.{{main_factory}} = success;
         });
         {% endif %}
         {% for factory in factories %}

            ctrl_page.fk_{{factory}} = {}

            // we must prevent calling backend continuously because results are returned asynchronously
            ctrl_page.loadFK_{{factory}} = function(id) {
                // if {{main_factory}} is returned (when it is not, template calls this method with undefined id)
                if (id != undefined) {
                    // call only once for each {{factory}} id
                    if (ctrl_page.fk_{{factory}}[id] === undefined) {
                        // mark that call has been made but value is null because result is not returned yet
                        ctrl_page.fk_{{factory}}[id] = null;
                        {{factory | title}}Factory.getById(id).then(function (success) {
                            // save the result once it is returned
                            ctrl_page.fk_{{factory}}[id] = success;
                            return success;
                        });
                    }
                    // if we already have the result return it
                    else return ctrl_page.fk_user[id];
                }
            }
         {% endfor %}
    }


})();