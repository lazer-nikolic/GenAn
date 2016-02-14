'''
Created on 08.02.2016.

@author: Lazar
'''


class SelectorView(object):
    '''
    classdocs
    '''

    def __init__(self, view, parent):
        parent.selector = self
        self.view = view
        self.parent = parent

