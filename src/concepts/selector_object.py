'''
Created on 08.02.2016.

@author: Lazar
'''
from textx.exceptions import TextXSemanticError

        
def selector_object_processor(selector_object):
    if selector_object.property not in selector_object.object.properties:
        line, col = selector_object._tx_metamodel.parser.pos_to_linecol(
            selector_object._tx_position)
        raise TextXSemanticError("ERROR: (at %d, %d) Object %s has no property named %s." %
                                 (line, col, selector_object.object.name, selector_object.property.name))
    else:
        return True

class SelectorObject(object):
    '''
    classdocs
    '''

    def __init__(self, object, property, parent, query=None):
        self.object = object
        self.property = property
        self.query = query
        self.parent = parent

