var express = require('express');
var router = express.Router();

var mongoose = require('mongoose');
var {{o.name|title}} = require('../models/{{o.name|title}}.js');

/* GET /users listing. */
router.get('/', function(req, res, next) {
{{o.name|title}}.find({}).populate('author')
  .exec(function (err, post) {
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