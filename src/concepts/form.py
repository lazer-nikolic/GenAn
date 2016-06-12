'''
Created on 08.02.2016.

@author: Lazar
'''
from textx.exceptions import TextXSemanticError

class Form(object):
    '''
    classdocs
    '''

    def __init__(self, parent, obj, actions):
        self.obj = obj
        self.actions = actions
        self.parent = parent
        self.name = obj.obj_name + "_form"
        self.subviews = []

    def accept(self, visitor):
        return visitor.visit_action_selector(self.obj, self.actions)
