'''
Created on 08.02.2016.

@author: Lazar
'''
from textx.exceptions import TextXSemanticError

        
def selector_object_processor(selector_object):
    if not selector_object.property in selector_object.object.properties:
        raise TextXSemanticError("object '{0}' has no attribute named '{1}'".format(selector_object.object.name, selector_object.property.name) )
    else:
        return True

class SelectorObject(object):
    '''
    classdocs
    '''

    def __init__(self, object, property,parent, query=None):
        self.object = object
        self.property = property
        self.query = query
        self.parent = parent
