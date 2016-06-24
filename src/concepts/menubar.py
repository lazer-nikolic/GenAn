'''
Created on 08.02.2016.

@author: Lazar
'''

def menubar_processor(menubar_object):
    if not menubar_object.brandLink is None:
        menubar_object.brandLink = '#/'+menubar_object.brandLink.page.name
    else:
        menubar_object.brandLink = '#';

class Menubar(object):
    '''
    classdocs
    '''

    def __init__(self, menus, parent, brandName, color, name, brandLink):
        self.menus = menus
        self.parent = parent
        self.brandName = brandName
        self.color=color
        self.name = name
        self.brandLink = brandLink