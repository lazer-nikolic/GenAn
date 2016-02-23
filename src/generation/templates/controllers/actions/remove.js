ctrl.remove = function () {
    {{form.name | title}}Factory.remove(ctrl.currentObject.id);
    EventBus.emitEvent('index');
}