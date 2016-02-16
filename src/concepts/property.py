'''
Created on 08.02.2016.

@author: Lazar
'''

class Property(object):
    '''
    classdocs
    '''

    def __init__(self, name, type, param, params, label, parent, classes):
        self.name = name
        self.type = type
        self.param = param
        self.label = label
        self.parent = parent       
        self.params = params       
        self.classes = classes
        