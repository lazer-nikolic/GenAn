'''
Created on 08.02.2016.

@author: Kupco
'''
from textx.exceptions import TextXSemanticError


def selector_fk_object_processor(selector_fk_object):
    # if selector_fk_object.property not in selector_fk_object.object.properties:
    #     line, col = selector_fk_object._tx_metamodel.parser.pos_to_linecol(
    #         selector_fk_object._tx_position)
    #     raise TextXSemanticError("ERROR: (at %d, %d) Object %s has no property named %s." %
    #                              (line, col, selector_fk_object.object.name, selector_fk_object.property))
    # else:
        return True


class SelectorFKObject(object):
    '''
    classdocs
    '''

    def __init__(self, object, property, fkProperties, parent):
        self.object = object
        self.property = property
        self.fkProperties = fkProperties
        self.parent = parent
        self.name = object.obj_name

    def accept(self, visitor):
        return visitor.visit_selector_fk_object(self.object, self.property)