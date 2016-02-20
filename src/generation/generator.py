'''
Created on 08.02.2016.

@author: Lazar
'''
import json
import subprocess
import zipfile

import shutil

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
                                               os.path.join("..", "generation", "templates", "views", "basic"),
                                               os.path.join("..", "generation", "templates", "views", "data_show"),
                                               os.path.join("..", "generation", "templates", "views", "frame")
                                               ]))

    template = env.get_template("{0}".format(template_name))
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

        answer = input(BColors.OKBLUE + "GENAN:" + BColors.ENDC + 
                       " Do you want to generate node.js backend for your application? [y/n] ")
        while not answer.lower() in ["y", "n", "yes", " no"]:
            answer = input(BColors.OKBLUE + "GENAN:" + BColors.ENDC + 
                           " Do you want to generate node.js backend for your application? [y/n] ")

        if answer.lower() in ["y", "yes"]:
            self.app_name = input(BColors.OKBLUE + "GENAN:" + BColors.ENDC + 
                              " Name of your application (default: genanApp): ")
            if self.app_name == '':
                self.app_name = "genanApp"
            # Call express to set up node.js server
            try:
                print(self.path)
                base_path = os.path.join(self.path, self.app_name)
                if not os.path.exists(base_path):
                    os.makedirs(base_path)
                subprocess.check_call(["express"], shell=True, cwd=base_path)
                print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Installing dependencies...")
                subprocess.check_call(["npm", "install"], shell=True, cwd=base_path)
                subprocess.check_call(["npm", "install", "mongoose", "--save"],
                                      shell=True, cwd=base_path)
                subprocess.check_call(["npm", "install", "ejs", "--save"],
                                      shell=True, cwd=base_path)
                subprocess.check_call(["npm", "install", "debug", "--save"],
                                      shell=True, cwd=base_path)
                # Enable objects generation
                self.visitors['Object'] = self.generate_object
                print(BColors.OKGREEN + "SUCCESS:" + BColors.ENDC + " Finished the backend generation.")
            except subprocess.CalledProcessError:
                print(BColors.FAIL + "ERROR:" + BColors.ENDC + " Unable to generate the backend. Cleaning up...")
                shutil.rmtree(base_path)


    def generate(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if not os.path.exists(os.path.join(self.path, "app", "styles")):
            os.makedirs(os.path.join(self.path, "app", "styles"))
        shutil.copy(os.path.join(os.pardir, "generation", "templates", "views", "page.css"),
                    os.path.join(self.path, "app", "styles", "page.css"))
        try:
            for concept in self.model.concept:
                class_name = concept.__class__.__name__
                if class_name in self.visitors:
                    self.visitors[class_name](concept)

            if self.objects:
                render_app = get_template("app.js", objects=self.objects, app_name=self.app_name)
                app_file = open(os.path.join(self.path, self.app_name, "app.js"), "w+")
                print(render_app, file=app_file)
        except Exception as e:
            print(BColors.FAIL + e)
            print(BColors.FAIL + "ERROR:" + BColors.ENDC + " Generation failed. Cleaning up...")
            shutil.rmtree(self.path)


    def generate_basic(self, comp, o, prop):
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

            print("Generating view {0}".format(view.name))
            self.generate_ctrl(view)
            for selector in view.views:
                print(self.generate_selector(selector), file=file)

            rendered = get_template("view.html", views=views)
            print(rendered, file=file)

            return "<ng-include src={0}></ng-include>".format(view.name)

    def generate_page(self, page):
        # Contains contained views
        positions = {}
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

        print("Generating page {0}".format(page.name))
        self.generate_ctrl(page)
        for view_on_page in page.views:
            selector = view_on_page.selector
            # Default value is 'center'
            position = view_on_page.position if view_on_page.position else 'center'
            if position not in positions:
                positions[position] = []
            positions[position].append(self.generate_selector(selector))
        
        menuExist ='false'
        sidebarExist='false'    
        menuRender=""
        if not page.menubar is None:
            menuRight=[]
            menuLeft=[]
            menuExist='true'
            for x in page.menubar.menus:
                if len(x.side) == 0:
                    menuLeft.append(x)
                else:
                    if x.side[0] =='left':
                        menuLeft.append(x)
                    else:
                        menuRight.append(x)
            menuRender = get_template("header.html", menuRight=menuRight, menuLeft=menuLeft, brand_name=page.menubar.brandName)
            
        sidebarRend = ""
        if not page.sidebar is None:
            sidebarRend = get_template("sidebar.html", sidebar=page.sidebar, menu=menuExist)
            sidebarExist='true'

        footerRend = ""
        if not page.footer is None:
            footerRend = get_template("footer.html", footer=page.footer, sidebarExist=sidebarExist)
            
        rendered = get_template("page.html", page=page, positions=positions, sidebar=sidebarRend, footer=footerRend, header=menuRender)
        print(rendered, file=file)

    def generate_ctrl(self, concept):
        # TODO: Generate stuff
        print("Generating controller for {0}".format(concept.name))

    def generate_object_selector(self, o, prop):
        print("Generating object {0}".format(o.name))
        return self.generate_view(prop.type, o, prop)
    
    def generate_form(self, obj, action):
        formInputs = []
        for property in obj.properties:
            if property.type is 'image': #Za sliku se unosi string, a ne prikazuje se!
                render = get_template("text.html", o=obj, prop=property, type=property.type.name)
                formInputs.append(render)
            else:
                render = self.generate_basic(obj, obj, property)
                formInputs.append(render)
        return get_template("form.html", formInputs=formInputs, obj=obj,action=action)

    def generate_selector(self, selector):
        # SelectorView contains a view
        # SelectorObject contains an object
        
        if hasattr(selector, "view"):
            return self.generate_view(selector.view)
        elif hasattr(selector, "object"):
            return self.generate_object_selector(selector.object, selector.property)
        elif hasattr(selector, "type"):
            return get_template("{0}.html".format(selector.type.name), data=selector.data)
        elif hasattr(selector, "action"):
            return self.generate_form(obj=selector.obj,action = selector.action)
        else:
            print(BColors.FAIL + " selector '{0}' ERROR".format(selector))

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


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
