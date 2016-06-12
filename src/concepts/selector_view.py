'''
Created on 08.02.2016.

@author: Lazar
'''


class SelectorView(object):
    '''
    classdocs
    '''

    def __init__(self, view, parent):
        self.view = view
        self.parent = parent

    def accept(self, visitor):
        return visitor.visit_selector_view(self.view)
