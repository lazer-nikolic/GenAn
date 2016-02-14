'''
Created on 08.02.2016.

@author: Lazar
'''
import os
from concepts.view import View


class Generator(object):
    '''
    classdocs
    '''

    def __init__(self, model, builtins, path):
        self.path = path
        self.model = model
        self.builtins = builtins
        self.visitors = {
            'View': self.generate_view,
            'Page': self.generate_page,
            'Object': self.generate_object
        }

    def generate(self):
        #if not os.path.exists(self.path):
            #os.makedirs(self.path)
        for concept in self.model.concept:
            self.visitors[concept.__class__.__name__](concept)

    def generate_basic(self, comp):
        pass

    def generate_view(self, view):
        if view.name in self.builtins:
            self.generate_basic(view)
        else:
            pass

    def generate_page(self, page):
        pass

    def generate_object(self, object):
        pass