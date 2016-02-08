'''
Created on 08.02.2016.

@author: Lazar
'''

class Page(object):
    '''
    classdocs
    '''


    def __init__(self, name, title, views, parent):
        self.name = name
        self.title = title
        self.views = views
        self.parent = parent
        