
{% set model_name = o.name %}
/*
    Generated code for {{ model_name }} route callbacks, please do not modify.

    Use provided 'custom_route_callbacks' directory 
    for defining a custom behavior callback route function.
*/

var _ = require('lodash');
var mongoose = require('mongoose');
var {{ model_name }} = require('../../models/{{ model_name }}_model');
var queryOps = require('../../common');

var {{ model_name }}RouteCallbacks = {};

{{ model_name}}RouteCallbacks.getAll = function(req, res, next) {
    sort_field = '';
    sort = [];
    order = 'descending';
    queries = {};
    from = -1;
    to = -1;

    for (query in req.query){
        query_string = req.query[query];
        query_parts = query_string.split("$");

        console.log(query);
        console.log(query_string);

        // Reserved params
        if (query === 'sortBy'){
            sort_field = query_string;
            console.log(sort);
            continue;
        }

        if (query === 'order'){
            order = query_string;
            if (sort_field != ''){
                sort.push([sort_field, order]);
            }
            console.log(sort);
            continue;
        }

        if (query === 'from'){
            from = parseInt(query_string);
            continue;
        }

        if (query === 'to'){
            to = parseInt(query_string);
            continue;
        }


        if (query_parts.length > 1){
            param = query_parts[1];
            operation = query_parts[0];
            queryOp = queryOps[operation];
            newQuery = queryOp(operation, param);
            queries[query] = newQuery[operation];
        }
        else {
            queries[query] = req.query[query];
        }
    }

    _.merge(queries, req.params);

    query = {{ model_name }}.find(queries).sort(sort);
    if (from > -1){
        query.limit(to);
    }
    if (to > -1){
        query.skip(from);
    }

    query.exec(function (err, post) {
        if (err) return next(err);
            res.json(post);
        }
    );
};

{{ model_name }}RouteCallbacks.post = function(req, res, next) {
    {{ model_name }}.create(req.body, function (err, post) {
        if (err) { 
            return next(err);
        }
        res.json(post);
    });
};

{{ model_name }}RouteCallbacks.getById = function(req, res, next) {
    {{ model_name }}.findOne({ '_id' : req.params.{{ model_name }}_id })
        .exec(function (err, post) {
        if (err) {
            return next(err);
        }
        res.json(post);
    });
};

{{ model_name }}RouteCallbacks.putById = function(req, res, next) {
    {{ model_name }}.findByIdAndUpdate(req.params.{{ model_name }}_id, req.body, function (err, post) {
        if (err) {
            return next(err);
        }
        res.json(post);
    });
};

{{ model_name }}RouteCallbacks.deleteById = function(req, res, next) {
    {{ model_name }}.findByIdAndRemove(req.params.{{ model_name }}_id, req.body, function (err, post) {
        if (err) { 
            return next(err);
        }
        res.json(post);
    });
};

{% for fk in o.meta|selectattr('foreignKeyType', 'equalto', 'single') %}
    {{ model_name }}RouteCallbacks.get{{ fk.label }}= function(req, res, next) {
        {{ model_name }}.findOne({ '_id' : req.params.{{ model_name }}_id })
            .populate('{{ fk.label }}')
            .exec(function(err, post) {
                if(err) {
                    return next(err);
                }
                res.json(post.{{ fk.label }});
            });
    };
{% endfor %}

module.exports = {{ model_name }}RouteCallbacks;
