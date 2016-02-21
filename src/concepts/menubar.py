'''
Created on 08.02.2016.

@author: Lazar
'''


class Menubar(object):
    '''
    classdocs
    '''

    def __init__(self, menus, parent, brandName, color, name):
        self.menus = menus
        self.parent = parent
        self.brandName = brandName
        self.color=color
        self.name = name
