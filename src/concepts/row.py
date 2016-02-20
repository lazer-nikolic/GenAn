'''
Created on 08.02.2016.

@author: Lazar
'''


class Row(object):
    '''
    classdocs
    '''

    def __init__(self, selectors, parent):
        self.selectors = sorted(selectors, key=lambda selector: selector.position)
        self.parent = parent
