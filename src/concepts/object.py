'''
Created on 08.02.2016.

@author: Lazar
'''

# def object_processor(object):
#     for query in object.queries:
#         if query.property not in object.properties:
#             line, col = object._tx_metamodel.parser.pos_to_linecol(
#                 object._tx_position)
#             raise TextXSemanticError("ERROR: (at %d, %d) Object %s has no property named %s." %
#                                      (line, col, object.object.name, object.property.name))
#         elif query.sortBy not in object.properties:
#             line, col = object._tx_metamodel.parser.pos_to_linecol(
#                 object._tx_position)
#             raise TextXSemanticError("ERROR: (at %d, %d) Object %s has no property named %s." %
#                                      (line, col, object.object.name, object.property.name))
#         else:
#             return True

from concepts.property import Property
from concepts.view import View
from textx.exceptions import TextXSemanticError

def object_processor(object):
    #check if property exist for current object
    checkUnique = []
    for fk in object.meta:
        for prop in fk.property.properties:
           if prop not in fk.object.properties:
            line, col = fk.object._tx_metamodel.parser.pos_to_linecol(
                fk.object._tx_position)
            raise TextXSemanticError("ERROR: (at %d, %d) Object %s has no property named %s." %
                                     (line, col, fk.object.name, prop.name))

        #check if label is unique
        if fk.label in checkUnique:
            raise TextXSemanticError("ERROR: %s already exist. All labels in Meta must be unique."%fk.label)
        else:
            checkUnique.append(fk.label)

        #bind Meta to property
        if fk.foreignKeyType == 'list':
            newType = View(None, 'multilist', [], object)
        else:
            newType = View(None, 'combobox', [], object)

        newProperty = Property(fk.label, newType, fk.label, None, [])
        newProperty.dontShowInTable = True
        newProperty.populateFromDB = True
        newProperty.extraPropertyList=fk.property.properties
        object.properties.append(newProperty)


class Object(object):
    def __init__(self, properties, queries, meta, name, parent):
        self.properties = properties
        self.queries = queries
        self.name = name
        self.parent = parent
        self.meta = meta

    def accept(self, visitor):
        return visitor.visit_object(self)
