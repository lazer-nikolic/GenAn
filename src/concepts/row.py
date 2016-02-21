'''
Created on 08.02.2016.

@author: Lazar
'''


class Row(object):
    '''
    classdocs
    '''

    def __init__(self, parent, number=-1):
        self.parent = parent
        self.number = number
        self.selectors = []

    def sort_selectors(self):
        self.selectors = sorted(self.selectors, key=lambda selector: selector.position)