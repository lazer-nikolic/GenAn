
{% set model_name = o.name %}
/*
    Use this file to override generated routes for {{ model_name }}
    route callbacks.
    It is mandatory to use provided {{ model_name }}RouteCallbacks
    object to override one of the default REST methods:
        - getAll
        - getById
        - post
        - putById
        - deleteById

    and all of the GET methods for one on one relationships of {{ model_name }}:
    {% for fk in o.meta|selectattr('foreignKeyType', 'equalto', 'single') %}
        - get{{ fk.label|capitalize }}
    {% endfor %}
*/

var _ = require('lodash');
var mongoose = require('mongoose');
var {{ model_name }} = require('../../models/{{ model_name }}_model');
var queryOps = require('../../common');

var {{ model_name }}RouteCallbacks = require('../.default_route_callbacks/{{ model_name }}_default_route_callbacks');

/*
    Example code:

        {{ model_name }}RouteCallbacks.getAll(req, res, next) {
            res.json('Hello World!');
        }
*/


//    Write your custom route callback HERE!


module.exports = {{ model_name }}RouteCallbacks;

