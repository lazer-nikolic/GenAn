var mongoose = require('mongoose');
var Schema = mongoose.Schema;
var {{ o.name|title }}Schema = new mongoose.Schema({

{% for prop in o.properties %}
{% if prop.dontShowInTable != True %}
  {{ prop.name }}: {{ persistent_types[prop.type.name] if prop.type.name in persistent_types else 'String' }},
{% endif %}
{% endfor %}

{% for fk in o.meta %}
 {% if fk.foreignKeyType == 'list' %}
  {{ fk.label }}: [{ type: Schema.Types.ObjectId, ref: '{{fk.object.name|title}}' }],
 {% else %}
  {{ fk.label }}: { type: Schema.Types.ObjectId, ref: '{{fk.object.name|title}}' },
 {% endif %}
{% endfor %}

  updated_at: { type: Date, default: Date.now },
});

module.exports = mongoose.model('{{ o.name|title }}', {{ o.name|title }}Schema);
