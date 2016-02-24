'''
Created on 08.02.2016.

@author: Lazar
'''
import json
import subprocess
import zipfile

import shutil

import os
from concepts.row import Row
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
                                               os.path.join("..", "generation", "templates", "views", "frame"),
                                               os.path.join("..", "generation", "templates", "controllers"),
                                               os.path.join("..", "generation", "templates", "route")
                                               ]))

    template = env.get_template("{0}".format(template_name))
    return template.render(kwargs)


class Generator(object):
    '''
    classdocs
    '''

    def __init__(self, model, builtins, path, debug=False):
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
        if debug:
            answer = 'n'
        else:
            answer = input(BColors.OKBLUE + "GENAN:" + BColors.ENDC +
                           " Do you want to generate framework for your AngularJS application? [y/n] ")
            while not answer.lower() in ["y", "n", "yes", " no"]:
                answer = input(BColors.OKBLUE + "GENAN:" + BColors.ENDC +
                               " Do you want to generate framework for your AngularJS for your application? [y/n] ")

        if answer.lower() in ["y", "yes"]:
            seed_file = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'app.zip')
            try:
                zip_ref = zipfile.ZipFile(seed_file, 'r')
                zip_ref.extractall(self.path)
                zip_ref.close()
            except FileNotFoundError:
                print(BColors.FAIL + "ERROR:" + BColors.ENDC + " Unable to generate framework. Continues...")

        with open('config.json') as data_file:
            self.type_mapper = json.load(data_file)

        answer = input(BColors.OKBLUE + "GENAN:" + BColors.ENDC +
                       " Do you want to generate node.js backend for your application? [y/n] ")
        while not answer.lower() in ["y", "n", "yes", " no"]:
            answer = input(BColors.OKBLUE + "GENAN:" + BColors.ENDC +
                           " Do you want to generate node.js backend for your application? [y/n] ")

        if answer.lower() in ["y", "yes"]:
            # Call express to set up node.js server
            self.app_name = input(BColors.OKBLUE + "GENAN:" + BColors.ENDC +
                                  " Name of your application (default: genanApp): ")
            if self.app_name == '':
                self.app_name = "genanApp"

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
                subprocess.check_call(["npm", "install", "cors", "--save"],
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
        if not os.path.exists(os.path.join(self.path, "app", "src", "styles")):
            os.makedirs(os.path.join(self.path, "app", "src", "styles"))
        shutil.copy(os.path.join(os.pardir, "generation", "templates", "views", "page.css"),
                    os.path.join(self.path, "app", "src", "styles", "page.css"))
        try:
            for concept in self.model.concept:
                class_name = concept.__class__.__name__
                if class_name in self.visitors:
                    self.visitors[class_name](concept)
            self.generate_factories()
            self.generate_route_file()
            if self.objects:
                render_app = get_template("app.js", objects=self.objects, app_name=self.app_name)
                app_file = open(os.path.join(self.path, self.app_name, "app.js"), "w+")
                shutil.copy(os.path.join(os.pardir, "generation", "templates", "backend", "common.js"),
                            os.path.join(self.path, self.app_name))
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
            # Rows for this view
            rows = []

            file = self.form_route(view.name)
            self.generate_view_controller(view)
            print("Generating view {0}".format(view.name))

            for row in view.rows:
                rows.append((row.number, self.generate_row(row)))

            rendered = get_template("view.html", rows=rows)
            print(rendered, file=file)

            return "<div ui-view='{0}'></div>".format(view.name)

    def generate_page(self, page):
        # Contains contained views
        positions = {}

        file = self.form_route(page.name)
        self.add_subroutes(page)

        print("Generating page {0}".format(page.name))
        self.generate_page_controller(page)
        for view_on_page in page.views:
            selector = view_on_page.selector
            # Default value is 'center'
            position = view_on_page.position if view_on_page.position else 'center'
            if position not in positions:
                positions[position] = []
            positions[position].append(self.generate_selector(selector))

        menuExist = 'false'
        sidebarExist = 'false'
        menuRender = ""
        if not page.menubar is None:
            menuRight = []
            menuLeft = []
            menuExist = 'true'
            for x in page.menubar.menus:
                if len(x.side) == 0:
                    menuLeft.append(x)
                else:
                    if x.side[0] == 'left':
                        menuLeft.append(x)
                    else:
                        menuRight.append(x)
            menuRender = get_template("header.html", header=page.menubar, menuRight=menuRight, menuLeft=menuLeft)

        sidebarRend = ""
        if not page.sidebar is None:
            sidebarRend = get_template("sidebar.html", sidebar=page.sidebar, menu=menuExist)
            sidebarExist = 'true'

        footerRend = ""
        if not page.footer is None:
            footerRend = get_template("footer.html", footer=page.footer, sidebarExist=sidebarExist)

        rendered = get_template("page.html", page=page, positions=positions, sidebar=sidebarRend, footer=footerRend,
                                header=menuRender)
        print(rendered, file=file)

    def generate_ctrl(self, name, render):
        path = os.path.join(self.path, "app", "src", "app", "controllers", name)
        file_path = "{0}.controller.js".format(name)
        full_path = os.path.join(path, file_path)
        if not os.path.exists(path):
            os.makedirs(path)
        file = open(full_path, 'w+')
        print(render, file=file)
        print("Generating controller for {0}".format(name))

    def generate_object_selector(self, o, prop):
        print("Generating object {0}".format(o.name))
        return self.generate_view(prop.type, o, prop)

    def generate_form(self, obj, actions):
        formInputs = []
        self.generate_form_controller(obj, actions)
        for property in obj.properties:

            if property.type is 'image':  # Za sliku se unosi string, a ne prikazuje se!
                render = get_template("text.html", o=obj, prop=property, type=property.type.name)
                formInputs.append(render)
            else:
                render = self.generate_basic(obj, obj, property)
                formInputs.append(render)
        return get_template("form.html", formInputs=formInputs, obj=obj, actions=actions)

    def generate_selector(self, selector):
        # SelectorView contains a view
        # SelectorObject contains an object
        if hasattr(selector, "view"):
            return self.generate_view(selector.view)
        elif hasattr(selector, "object"):
            return self.generate_object_selector(selector.object, selector.property)
        elif hasattr(selector, "data"):
            return get_template("{0}.html".format(selector.type.name), data=selector.data)

        elif hasattr(selector, "actions"):
            return self.generate_form(obj=selector.obj, actions=selector.actions)
        elif hasattr(selector, "paragraph"):
            return get_template("paragraph.html", paragrpah=selector.paragraph)
        elif hasattr(selector, "jumbo"):
            return get_template("jumbo.html", jumbo = selector)
        elif hasattr(selector, "stLink"):
            return get_template("staticLink.html", link = selector.stLink, classes = selector.classes)
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

    def generate_row(self, row):
        print("Generating row... ")
        rendered_selector = {}
        for sub_view in row.selectors:
            rendered_selector[sub_view.selector] = self.generate_selector(sub_view.selector)
        row_selectors = [sub_view.selector for sub_view in row.selectors]
        return get_template("row.html", sub_views=row.selectors, rendered_selector=rendered_selector)

    def form_route(self, name):
        """
        form_route(self, name)
        Creates folder, file and forms route for a view or a page with passed name.
        Returns the after mentioned file.
        :param name:
        :return: Created file
        """

        path = os.path.join(self.path, "app", "src", "app", "views", name)
        file_path = "{0}.html".format(name)
        full_path = os.path.join(path, file_path)
        relative_path = "app/views/" + name + "/" + name + ".html"

        if not os.path.exists(path):
            os.makedirs(path)
        file = open(full_path, 'w+')

        self.routes[name] = {
            'name': name,
            'path': "/{0}".format(name),
            'template': relative_path,
            'controller': "{0}".format(name),
            'sub_routes': []
        }

        return file

    def add_subroutes(self, page):
        print(page.name)
        for view in page.subviews:
            print(view.name)
            if view.name in self.routes:
                self.routes[page.name]['sub_routes'].append(self.routes[view.name])
        print(self.routes[page.name])


    def generate_form_controller(self, form, actions):
        formInputs = []
        for property in form.properties:
            if property.type is 'checkbox':
                render = get_template("checkbox.js", name=property.name)
                formInputs.append(render)
            elif property.type is 'date':
                render = get_template("date.js", name=property.name)
                formInputs.append(render)

        render = get_template("form.js", form=form, formInputs=formInputs, actions=actions)
        self.generate_ctrl(form.name + ".form", render)

    def generate_page_controller(self, page):
        factories = {}
        query = 'getAll'
        for view_on_page in page.views:
            selector = view_on_page.selector
            if hasattr(selector, 'object'):
                if selector.object.name not in factories:
                    factories[selector.object.name] = query

        if hasattr(page, 'object') and page.query:
            factories[page.object.name] = page.query.name


        render = get_template("page.js", page=page, factories=factories)
        self.generate_ctrl(page.name, render)

    def generate_view_controller(self, view):
        factories = []
        for view_on_page in view.views:
            if hasattr(view_on_page, 'selector'):
                selector = view_on_page.selector
                if hasattr(selector, 'object'):
                    if selector.object.name not in factories:
                        factories.append(selector.object.name)
        render = get_template("view.js", view=view, factories=factories)
        self.generate_ctrl(view.name, render)

    def generate_factories(self):
        for concept in self.model.concept:
            if concept.__class__.__name__ == "Object":
                # for query in concept.queries:
                #     self.stringifyQuery(query)
                render = get_template("factory.js", object=concept, query=concept.queries)
                path = os.path.join(self.path, "app", "src", "app", "factories", concept.name)
                file_path = "{0}.factory.js".format(concept.name)
                full_path = os.path.join(path, file_path)
                if not os.path.exists(path):
                    os.makedirs(path)
                file = open(full_path, 'w+')
                print(render, file=file)
                print("Generating factory for {0}".format(concept.name))

    def generate_route_file(self):
        render_routes = get_template("app.routes.js", routes=self.routes)
        render_modules = get_template("app.modules.js", modules=self.routes)
        path = os.path.join(self.path, "app", "src", "app")
        file_path_routes = "app.routes.js"
        file_path_modules = "app.modules.js"
        full_path_routes = os.path.join(path, file_path_routes)
        full_path_modules = os.path.join(path, file_path_modules)
        if not os.path.exists(path):
            os.makedirs(path)
        file_routes = open(full_path_routes, 'w+')
        print(render_routes, file=file_routes)
        print("Generating app.route.js")
        file_modules = open(full_path_modules, 'w+')
        print(render_modules, file=file_modules)
        print("Generating app.modules.js")

    def stringifyQuery(self, query):
        string = ""
        if hasattr(query, 'property'):
            string += 'property=' + query.property.name + '&'
        if hasattr(query, 'condition'):
            string += 'condition=' + query.condition.conditionName+"$"+str(query.condition.parameter) + '&'
        if hasattr(query, 'sortBy') and query.sortBy is not None:
            string += 'sortBy=' + query.sortBy.name + '&'
        if hasattr(query, 'order') and query.order is not None:
            string += 'order=' + query.order + '&'
        if hasattr(query, 'rangeFrom'):
            string += 'from=' + str(query.rangeFrom) + '&'
        if hasattr(query, 'rangeTo') and query.rangeTo != 0:
            string += 'to=' + str(query.rangeTo) + '&'
        if len(string) > 0:
            string = string[:-1]
        query.string = string

class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
