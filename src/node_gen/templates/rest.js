var express = require('express');
var _ = require('lodash');

{#
    'mergeParams : true' is a compromise solution since it would be necessary to check whether is 
    entity's foreign key type of relation with some other entity. If it's always enabled, it is 
    possible to make nested routes if necessary.
#}
var router = express.Router({ mergeParams : true });    

var mongoose = require('mongoose');
{% set model_name = o.name %}
var {{ model_name }} = require('../models/{{ model_name }}.js');
var queryOps = require('../common');

{%+ for fk_type in o.meta|selectattr('foreignKeyType', 'equalto', 'list')|unique_types %}
    var {{ fk_type|router_var }} = require('./{{ fk_type }}.js');
{% endfor %}

{%+ for fk in o.meta|selectattr('foreignKeyType', 'equalto', 'list') %}
    router.use('/:{{ model_name }}_id/{{ fk.label }}', {{ fk.object.name|router_var }});
{% endfor %} 

/* GET /{{ model_name }} */
router.get('/'
, function(req, res, next) {
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
});

/* POST /{{ model_name }} */
router.post('/', function(req, res, next) {
  {{ model_name }}.create(parameters, function (err, post) {
    if (err) return next(err);
    res.json(post);
  });
})

/* GET /{{ model_name }}/{{ model_name }}_id */
router.get('/:{{ model_name }}_id', function(req, res, next) {
  {{ model_name }}.findOne({ '_id' : req.params.{{ model_name }}_id })
    .exec(function (err, post) {
      if (err) return next(err);
      res.json(post);
    }
  );
});

/* PUT /{{ model_name }}/:{{ model_name }}_id */
router.put('/:{{ model_name }}_id', function(req, res, next) {
  {{ model_name }}.findByIdAndUpdate(req.params.{{ model_name }}_id, req.body, function (err, post) {
    if (err) return next(err);
    res.json(post);
  });
});

/* DELETE /{{ model_name }}/:{{ model_name }}_id */
router.delete('/:{{ model_name }}_id', function(req, res, next) {
  {{ model_name }}.findByIdAndRemove(req.params.{{ model_name }}_id, req.body, function (err, post) {
    if (err) return next(err);
    res.json(post);
  });
});

{% for fk in o.meta|selectattr('foreignKeyType', 'equalto', 'single') %}
/* GET /{{ model_name }}/{{ model_name }}_id/{{ fk.label }} */
router.get('/:{{ model_name }}_id/{{ fk.label }}', function(req, res, next) {
    {{ model_name }}.findOne({ '_id' : req.params.{{ model_name }}_id })
        .populate('{{ fk.label }}')
        .exec(function(err, post) {
            if(err) {
                return next(err);
            }
            res.json(post.{{ fk.label }});
        });
});
{% endfor %}

module.exports = router;
