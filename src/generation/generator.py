'''
Created on 08.02.2016.

@author: Lazar
'''
import json
import subprocess
import zipfile

import os
from jinja2 import Environment, PackageLoader, FileSystemLoader


def get_template(template_name, **kwargs):
    """
    get_template(template_name, **kwargs)
    Gets template under generation/templates folder and its subfolders.
    Takes additional parameters required for the template to be rendered.
    """
    env = Environment(trim_blocks=True, lstrip_blocks=True,
                      loader=FileSystemLoader([os.path.join("..", "generation", "templates"),
                                               os.path.join("..", "generation", "templates", "views"),
                                               os.path.join("..", "generation", "templates", "backend"),
                                               os.path.join("..", "generation", "templates", "views", "basic")
                                               ]))

    template = env.get_template(template_name)
    return template.render(kwargs)


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
            'Page': self.generate_page
        }

        # List of objects required for backend routes
        self.objects = []
        self.routes = {}

        with open('config.json') as data_file:
            self.type_mapper = json.load(data_file)

        answer = input("GENAN: Do you want to generate node.js backend for your application? [y/n] ")
        while not answer.lower() in ["y", "n", "yes", " no"]:
            answer = input("GENAN: Do you want to generate node.js backend for your application? [y/n] ")

        self.app_name = input("GENAN: Name of your application (default: genanApp): ")
        if self.app_name == '':
            self.app_name = "genanApp"

        if answer.lower() in ["y", "yes"]:
            # Call express to set up node.js server
            try:
                base_path = os.path.join(self.path, self.app_name)
                subprocess.check_call(["express", base_path], shell=True)
                print("GENAN: Installing dependencies...")
                subprocess.check_call(["npm", "install"], shell=True, cwd=base_path)
                subprocess.check_call(["npm", "install", "mongoose", "--save"],
                                      shell=True, cwd=base_path)
                subprocess.check_call(["npm", "install", "ejs", "--save"],
                                      shell=True, cwd=base_path)
                subprocess.check_call(["npm", "install", "debug", "--save"],
                                      shell=True, cwd=base_path)
                # Enable objects generation
                self.visitors['Object'] = self.generate_object
                print("GENAN: Finished the backend generation.")
            except subprocess.CalledProcessError:
                print("ERROR: Unable to generate the backend. Terminating process.")
                # TODO: Rollback


    def generate(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        for concept in self.model.concept:
            class_name = concept.__class__.__name__
            if class_name in self.visitors:
                self.visitors[class_name](concept)

        if self.objects:
            render_app = get_template("app.js", objects=self.objects, app_name=self.app_name)
            app_file = open(os.path.join(self.path, self.app_name, "app.js"), "w+")
            print(render_app, file=app_file)

    def generate_basic(self, comp, o, prop):
        if prop.type.name is "option" or prop.type.name is "menuItem":
            print("Property type escaped.")
            return

        return get_template("{0}.html".format(prop.type), o=o, prop=prop, type=prop.type.name)

    def generate_view(self, view, o=None, prop=None):

        if view.name in self.builtins:
            return self.generate_basic(view, o, prop)
        else:
            # Subviews for this view
            views = []
            path = os.path.join(self.path, "app", "views", view.name)
            file_path = "{0}.html".format(view.name)
            full_path = os.path.join(path, file_path)
            self.routes[view.name] = {
                'path': "/{0}".format(view.name),
                'template': "/{0}".format(full_path),
                'controller': "{0}Ctrl".format(view.name).title()
            }
            if not os.path.exists(path):
                os.makedirs(path)
            file = open(full_path, 'w+')

            print("Generating view {0} into {1}".format(view.name, full_path))
            self.generate_ctrl(view)
            for selector in view.views:
                print(self.generate_selector(selector), file=file)

            rendered = get_template("view.html", views=views)
            print(rendered, file=file)

            return "<ng-include src={0}></ng-include>".format(view.name)

    def generate_page(self, page):
        # Contains contained views
        views = []
        path = os.path.join(self.path, "app", "views", page.name)
        file_path = "{0}.html".format(page.name)
        full_path = os.path.join(path, file_path)
        self.routes[page.name] = {
            'path': "/{0}".format(page.name),
            'template': "/{0}".format(full_path),
            'controller': "{0}Ctrl".format(page.name).title()
        }

        if not os.path.exists(path):
            os.makedirs(path)
        file = open(full_path, 'w+')

        print("Generating page {0} into {1}".format(page.name, full_path))
        self.generate_ctrl(page)
        for view_on_page in page.views:
            selector = view_on_page.selector
            views.append(self.generate_selector(selector))

        rendered = get_template("page.html", page=page, views=views)

        print(rendered, file=file)

    def generate_ctrl(self, concept):
        # TODO: Generate stuff
        print("Generating controller for {0}".format(concept.name))

    def generate_object_selector(self, o, prop):
        return self.generate_view(prop.type, o, prop)

    def generate_selector(self, selector):
        # SelectorView contains a view
        # SelectorObject contains an object
        if hasattr(selector, "view"):
            return self.generate_view(selector.view)
        elif hasattr(selector, "object"):
            return self.generate_object_selector(selector.object, selector.property)

    def generate_object(self, object):
        '''
        generate_object(self, object)
        Generates a node.js rest service, route and model for an object.
        :param object:
        :return:
        '''
        base_path = os.path.join(self.path, self.app_name)
        models_path = os.path.join(base_path, "models")
        routes_path = os.path.join(base_path, "routes")

        rendered_model = get_template("model.js", o=object, persistent_types=self.type_mapper)
        rendered_rest = get_template("rest.js", o=object)

        if not os.path.exists(models_path):
            os.makedirs(models_path)

        if not os.path.exists(routes_path):
            os.makedirs(routes_path)

        file_model = open(os.path.join(models_path, "{0}.js".format(object.name)), 'w+')
        print(rendered_model, file=file_model)
        file_rest = open(os.path.join(routes_path, "{0}.js".format(object.name)), 'w+')
        print(rendered_rest, file=file_rest)
        self.objects.append(object)
