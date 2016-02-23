{% import 'common.jinja' as common %}
(function () {
    'use strict';

    angular
        .module('app')
        .factory('{{object.name | title}}Factory', {{object.name | title}}Factory);

    {{object.name | title}}Factory.$inject = ['ApiService'];

    function {{object.name | title}}Factory(ApiService) {

        var service = this;
        var relativeUrl = "{{object.name}}";

        function getAll() {
            return ApiService.getAll(relativeUrl);
        }

        function getById(id) {
            return ApiService.getById(relativeUrl, id);
        }

        function create(single_{{object.name}}) {
            return ApiService.create(relativeUrl, single_{{object.name}}, single_{{object.name}}._id);
        }

        function update(single_{{object.name}}) {
            return ApiService.update(relativeUrl, single_{{object.name}}, single_{{object.name}}._id);
        }

        function remove(id) {
            return ApiService.remove(relativeUrl, id);
        }

        <% for query in queries %>
        function {{query.name}}() {
            return ApiService.getQuery("{{query.string}}");
        }
        <% endfor %>

        return {
            getAll: getAll,
            getById: getById,
            create: create,
            update: update,
            remove: remove
        };
    }
})();