'''
Created on 08.02.2016.

@author: Lazar
'''

class View:
    basic_type_names = ['text', 'number', 'check', 'option', 'link', 'ref', 'email', 'password', 'menuitem', 'menu', 'button', 'radio', 'form', 'label', 'image']
    
    def __init__(self, parent, name, views):
        self.name = name
        self.views = views
        self.parent = parent

    def __str__(self):
        return self.name
        