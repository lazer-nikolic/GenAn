var express = require('express');

{#
    'mergeParams : true' is a compromise solution since it would be necessary to check whether is 
    entity's foreign key type of relation with some other entity. If it's always enabled, it is 
    possible to make nested routes if necessary.
#}
var router = express.Router({ mergeParams : true });    

{% set model_name = o.name %}
var {{ model_name }}RouteCallbacks = require('./route_callbacks/{{ model_name }}_route_callbacks.js');

{%+ for fk_type in o.meta|selectattr('foreignKeyType', 'equalto', 'list')|unique_types %}
    var {{ fk_type|router_var }} = require('./{{ fk_type }}_route.js');
{% endfor %}

{%+ for fk in o.meta|selectattr('foreignKeyType', 'equalto', 'list') %}
    router.use('/:{{ model_name }}_id/{{ fk.label }}', {{ fk.object.name|router_var }});
{% endfor %} 

/* GET /{{ model_name }} */
router.get('/', {{ model_name }}RouteCallbacks.getAll);

/* POST /{{ model_name }} */
router.post('/', {{ model_name }}RouteCallbacks.post);

/* GET /{{ model_name }}/{{ model_name }}_id */
router.get('/:{{ model_name }}_id', {{ model_name }}RouteCallbacks.getById);

/* PUT /{{ model_name }}/:{{ model_name }}_id */
router.put('/:{{ model_name }}_id', {{ model_name }}RouteCallbacks.putById);

/* DELETE /{{ model_name }}/:{{ model_name }}_id */
router.delete('/:{{ model_name }}_id', {{ model_name }}RouteCallbacks.deleteById);

{% for fk in o.meta|selectattr('foreignKeyType', 'equalto', 'single') %}
/* GET /{{ model_name }}/{{ model_name }}_id/{{ fk.label }} */
router.get('/:{{ model_name }}_id/{{ fk.label }}', {{ model_name }}RouteCallbacks.get{{ fk.label }});
{% endfor %}

module.exports = router;
