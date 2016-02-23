var express = require('express');
var router = express.Router();

var mongoose = require('mongoose');
var {{o.name|title}} = require('../models/{{o.name|title}}.js');
var queryOps = require('../common')

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
query = {{o.name|title}}.find(queries).sort(sort);
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
  {{o.name|title}}.create(req.body, function (err, post) {
    if (err) return next(err);
    res.json(post);
  });
})

/* GET /users/id */
router.get('/:id', function(req, res, next) {
{{o.name|title}}.findOne(req.params.id)
  .exec(function (err, post) {
      if (err) return next(err);
      res.json(post);
    }
  );
});

/* PUT /users/:id */
router.put('/:id', function(req, res, next) {
  {{o.name|title}}.findByIdAndUpdate(req.params.id, req.body, function (err, post) {
    if (err) return next(err);
    res.json(post);
  });
});

/* DELETE /users/:id */
router.delete('/:id', function(req, res, next) {
  {{o.name|title}}.findByIdAndRemove(req.params.id, req.body, function (err, post) {
    if (err) return next(err);
    res.json(post);
  });
});

module.exports = router;