'''
Created on 08.02.2016.

@author: Lazar
'''
from textx.exceptions import TextXSemanticError

def property_processor(property_object):
    
    adapter_property(property_object)
    ref_prop =['link', 'button','image']
    for type in ref_prop:
        if type is property_object.type.name:
            if property_object.ref is '' or property_object.ref is None:
                if type is 'link' and not property_object.ref_param is None:
                    property_object.ref = "#/"+property_object.ref_param.page.name 
                else:
                    raise TextXSemanticError("Type {0} must have ref='example.com' / @refToPage - for link".format(property_object.type))
            else:
                if type is 'link' and not property_object.ref_param is None:
                    raise TextXSemanticError("Type {0} can't have both type for link. Property name: {1}".format(property_object.type,property_object.name))
        
    parameters_allowed_fields=['combobox', 'checkbox', 'radio'] 
    for type in parameters_allowed_fields:
        if property_object.type.name not in parameters_allowed_fields:
            if not property_object.params is None:
                raise TextXSemanticError("Property {0} can't have parameters attribute.".format(property_object.type.name))
    
    classesString = "";
    if not property_object.classes is None:
        for x in property_object.classes.htmlClasses:
            if hasattr(x, 'value'):
                classesString += " " + x.key + "=\"" + x.value + "\"";
            else:
                classesString += " " + x.key;
        property_object.classes = classesString
    else:
        property_object.classes = ""


def adapter_property(property):
    '''
    Adapter method for additional parametes on property class
    '''
    
    for x in property.additionalParameters:
        if not x.ref_param is None:
            if not property.ref_param is None:
                raise TextXSemanticError("You can't use more than one @ link.")
            property.ref_param = x.ref_param
        elif not x.params is None:
            if not property.params is None:
                raise TextXSemanticError("You can't use more than one parameters keyword.")
            property.params = x.params
        elif not x.classes is None:
            if not property.classes is None:
                raise TextXSemanticError("You can't use more than one class keyword.")
            property.classes = x.classes
        elif not x.ref is None:
            if not property.ref is None:
                raise TextXSemanticError("You can't use more than one ref keyword.")
            property.ref = x.ref
  


class Property(object):
    '''
    classdocs
    '''

    def __init__(self, name, type, label, parent, additionalParameters):
        self.name = name
        self.type = type
        self.ref_param = None
        self.label = label
        self.parent = parent
        self.additionalParameters=additionalParameters
        self.params = None
        self.classes = None
        self.ref = None
        