'''
Created on 08.02.2016.

@author: Lazar
'''


class Menu(object):
    '''
    classdocs
    '''

    def __init__(self, name, items, parent, ref, side):
        self.name = name
        self.items = items
        self.parent = parent
        self.ref = ref
        self.side = side
