'''
Created on 08.02.2016.

@author: Lazar
'''
def property_processor(property_object):
    classesString ="";
    if not property_object.classes is None:
        for x in property_object.classes.htmlClasses:
            if hasattr(x, 'value'):
                classesString+=" "+x.key+"=\""+x.value+"\"";
            else:
                classesString+=" "+x.key;
        property_object.classes=classesString
    else:
        property_object.classes=""
        
class Property(object):
    '''
    classdocs
    '''

    def __init__(self, name, type, ref_param, params, label, parent, classes):
        self.name = name
        self.type = type
        self.ref_param = ref_param
        self.label = label
        self.parent = parent       
        self.params = params       
        self.classes = classes
        