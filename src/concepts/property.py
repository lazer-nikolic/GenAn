'''
Created on 08.02.2016.

@author: Lazar
'''
from textx.exceptions import TextXSemanticError

def property_processor(property_object):
    ref_prop =['link', 'button','image']
    for type in ref_prop:
        if type is property_object.type.name:
            if property_object.ref is '':
                if type is 'link' and not property_object.ref_param is None:
                    property_object.ref = "#/"+property_object.ref_param.page.name 
                else:
                    raise TextXSemanticError("Type {0} must have ref='example.com' / @refToPage - for link".format(property_object.type))
    
    
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


class Property(object):
    '''
    classdocs
    '''

    def __init__(self, name, type, ref_param, params, label, parent, classes, ref):
        self.name = name
        self.type = type
        self.ref_param = ref_param
        self.label = label
        self.parent = parent
        self.params = params
        self.classes = classes
        self.ref = ref