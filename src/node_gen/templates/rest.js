var express = require('express');

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

{% for fk_type in o.meta|unique_types %}
    var {{ fk_type|router_var }} = require('./{{ fk_type }}.js');
{% endfor %}

{% for fk in o.meta %}
    router.use('/:id/{{ fk.label }}', {{ fk.object.name|router_var }});
{% endfor %} 

/* GET /users listing. */
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
query = {{model_name}}.find(queries).sort(sort);
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

/* POST /users */
router.post('/', function(req, res, next) {
  {{ model_name }}.create(req.body, function (err, post) {
    if (err) return next(err);
    res.json(post);
  });
})

/* GET /users/id */
router.get('/:id', function(req, res, next) {
  {{ model_name }}.findOne({ '_id' : req.params.id })
    .exec(function (err, post) {
      if (err) return next(err);
      res.json(post);
    }
  );
});

/*
{% for fk in o.meta %}
//This should be changed
router.get('/:id/{{fk.label}}', function(req, res, next) {
{{model_name}}.findOne(req.params.id)
  .exec(function (err, post) {
      if (err) return next(err);
      res.json(post);
    }
  );
});
{% endfor %}
*/

/* PUT /users/:id */
router.put('/:id', function(req, res, next) {
  {{ model_name }}.findByIdAndUpdate(req.params.id, req.body, function (err, post) {
    if (err) return next(err);
    res.json(post);
  });
});

/* DELETE /users/:id */
router.delete('/:id', function(req, res, next) {
  {{ model_name }}.findByIdAndRemove(req.params.id, req.body, function (err, post) {
    if (err) return next(err);
    res.json(post);
  });
});

module.exports = router;
