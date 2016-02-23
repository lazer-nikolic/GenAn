
from textx.exceptions import TextXSemanticError

def query_processor(query):
    for query in query.parent.queries:
        if query.property not in query.parent.properties:
            line, col = query.parent._tx_metamodel.parser.pos_to_linecol(
                object._tx_position)
            raise TextXSemanticError("ERROR: (at %d, %d) Object %s has no property named %s." %
                                     (line, col, query.parent.object.name, query.parent.property.name))
        elif query.sortBy not in query.parent.properties:
            line, col = query.parent._tx_metamodel.parser.pos_to_linecol(
                object._tx_position)
            raise TextXSemanticError("ERROR: (at %d, %d) Object %s has no property named %s." %
                                     (line, col, query.parent.object.name, query.parent.property.name))
        else:
            return True

class Query(object):
    def __init__(self, parent, name, property=None, condition=None,sortBy=None, order=None, rangeFrom=None, rangeTo=None ):
        self.name = name
        self.parent = parent
        self.property = property
        self.condition = condition
        self.sortBy = sortBy
        self.order=order
        self.rangeFrom = rangeFrom
        self.rangeTo = rangeTo