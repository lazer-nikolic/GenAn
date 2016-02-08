'''
Created on 08.02.2016.

@author: Lazar
'''

class Object(object):
    '''
    classdocs
    '''


    def __init__(self, properties, name, parent):
        self.properties = properties
        self.name = name
        self.parent = parent
        