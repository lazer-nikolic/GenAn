'''
Created on 08.02.2016.

@author: Lazar
'''


class ViewInView(object):
    '''
    classdocs
    '''

    def __init__(self, selector, parent, position=1, size=0):
        self.selector = selector
        self.position = position
        self.size = size
        self.parent = parent
