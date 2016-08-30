var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

// Resources routes are required from separate files
var routes = require('./routes/index');
{% for object in objects %}
var {{object.name}} = require('./routes/{{object.name}}');
{% endfor %}

// MongoDB connection using Mongoose
var mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/{{ app_name }}', function(err) {
    if(err) {
        console.log('Connection error. Make sure you have run Mongo daemon and created connection.', err);
    } else {
        console.log('Successfully connected on {{ app_name }} database.');
    }
});

cors = require('cors')

var app = express();

app.use(cors());

// Uncomment lines bellow if you want to use Express API with a template engine (default engine is jade)
/*
    app.set('views', path.join(__dirname, 'views'));
    app.set('view engine', 'jade');
*/

app.use('/', routes);

{% for object in objects %}
app.use('/{{object.name}}', {{object.name}});
{% endfor %}

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.json('error', {
      message: err.message,
      error: err
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.json('error', {
    message: err.message,
    error: {}
  });
});


module.exports = app;
