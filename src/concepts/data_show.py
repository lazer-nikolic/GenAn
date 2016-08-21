'''
Created on 08.02.2016.

@author: Lazar
'''
from textx.exceptions import TextXSemanticError

def data_show_processor(data_show_object):
    data_show_kwd = ['table', 'list', 'thumbnail']
    for type in data_show_kwd:
        if type is data_show_object.type.name:
            return True
    else:
        raise TextXSemanticError("'{0}' is not avlaible. Correct keywords are 'table', 'list' or 'thumbnail'".format(data_show_object.type))


class DataShow(object):
    '''
    classdocs
    '''

    def __init__(self, type, parent, data):
        self.data = []
        for s in data:
            selector = s.so if s.so else s.sol
            self.data.append(selector)
        self.type = type
        self.parent = parent


    def accept(self, visitor):
        return visitor.visit_other_selector(self.type.name, data=self.data)
