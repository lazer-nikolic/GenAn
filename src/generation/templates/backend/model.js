{% import 'common.jinja' as common %}
var mongoose = require('mongoose');
var Schema = mongoose.Schema;
var {{o.name|title}}Schema = new mongoose.Schema({
{% for prop in o.properties %}
  {{prop.name}}: {{persistent_types[prop.type.name]}}
{% endfor %}
  updated_at: { type: Date, default: Date.now },
});

module.exports = mongoose.model('{{o.name|title}}', {{o.name|title}}Schema);