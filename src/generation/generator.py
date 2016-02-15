'''
Created on 08.02.2016.

@author: Lazar
'''
import os
from jinja2 import Environment, PackageLoader, FileSystemLoader


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
        # if not os.path.exists(self.path):
        #     os.makedirs(self.path)
        for concept in self.model.concept:
            class_name = concept.__class__.__name__
            self.visitors[class_name](concept)

    def generate_basic(self, comp, o, prop):
        # TODO: Generate stuff
        #print("Generating basic component {0}".format(comp.name))
        if prop.type.name is "option":
            print("Property type is option.")
            return;
        
        env = Environment(trim_blocks=True, lstrip_blocks=True,
                          loader=FileSystemLoader([os.path.join("..", "generation", "templates"),
                                                   os.path.join("..", "generation", "templates", "views", "basic")
                                                   ]))
        
        template = env.get_template("{0}.html".format(prop.type))
        rendered = template.render(o=o, prop=prop, type=prop.type.name)
        print(rendered)

    def generate_view(self, view, o, prop):
        if view.name in self.builtins:
            self.generate_basic(view, o, prop)
        else:
            # TODO: Generate stuff
            print("Generating view {0}".format(view.name))
            self.generate_ctrl(view)
            for selector in view.views:
                self.generate_selector(selector)

    def generate_page(self, page):
        # TODO: Generate stuff
        print("Generating page {0}".format(page.name))
        self.generate_ctrl(page)
        for view_on_page in page.views:
            selector = view_on_page.selector
            self.generate_selector(selector)

    def generate_ctrl(self, concept):
        # TODO: Generate stuff
        print("Generating controller for {0}".format(concept.name))

    def generate_object(self, object):
        # TODO: Generate stuff
        print("Generating object {0}".format(object.name))
        for prop in object.properties:
            self.generate_view(prop.type, object, prop)

    def generate_selector(self, selector):
        # SelectorView contains a view
        # SelectorObject contains an object
        if hasattr(selector, "view"):
            self.generate_view(selector.view, selector.object, selector.property)
        elif hasattr(selector, "object"):
            self.generate_object(selector.object, selector.object, selector.property)
