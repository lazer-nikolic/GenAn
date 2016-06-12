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

class Object(object):
    def __init__(self, properties, queries, name, parent):
        self.properties = properties
        self.queries = queries
        self.name = name
        self.parent = parent

    def accept(self, visitor):
        return visitor.visit_object(self)
