ctrl.save = function () {
    if (ctrl.update) {
        {{form.name | title}}Factory.update(ctrl.currentObject);
        angular.copy(ctrl.currentObject, ctrl.oldObject);
    } else {
        {{form.name | title}}Factory.save(ctrl.currentObject);
        angular.copy(ctrl.currentObject, ctrl.oldObject);
    }
}