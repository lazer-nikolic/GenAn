(function () {
    'use strict';

    angular
        .module('app.api')
        .service('ApiService', ApiService);
    ApiService.$inject = ['$http', '$q'];

    function ApiService($http, $q) {

        var baseUrl = "{{backend_url}}";

        function getAll(relativeUrl) {
            var deferred = $q.defer();

            var url = baseUrl + relativeUrl;
            $http.get(url).success(function (data) {
                deferred.resolve(data);
            });

            return deferred.promise;
        }

        function getById(relativeUrl, id) {

            var deferred = $q.defer();

            var url = baseUrl + relativeUrl + "/" + id;

            $http.get(url).success(function (data) {
                deferred.resolve(data);
            });

            return deferred.promise;
        }

        function create(relativeUrl, object) {

            var url = baseUrl + relativeUrl;
            $http({
                method: 'POST',
                url: url,
                data: object,
                headers: {'Content-Type': 'application/json'}
            }).success(function (data) {
                //
            });
        }


        function update(relativeUrl, object, id) {

            var url = baseUrl + relativeUrl + "/" + id;

            $http({
                method: 'PUT',
                url: url,
                data: object,
                headers: {'Content-Type': 'application/json'}
            }).success(function (data) {
               //
            });
        }

        function remove(relativeUrl, id) {

            var url = baseUrl + relativeUrl + "/" + id;

            $http.delete(url).success(function (data) {
                //
            });
        }

        function getQuery(relativeUrl, query) {
            var deferred = $q.defer();

            var url = baseUrl + relativeUrl + '?' + query;
            $http.get(url).success(function (data) {
                deferred.resolve(data);
            });

            return deferred.promise;
        }

        return {
            getAll: getAll,
            getById: getById,
            create: create,
            update: update,
            remove: remove,
            getQuery: getQuery
        }

    }
}());