import json
import subprocess

import os
import shutil
from angular_gen.jinja_filters import sub_routes_filter
from jinja2 import FileSystemLoader, Environment
from main.common import BColors, BackendGenerator
from node_gen.jinja_filters import *

_MSG_HEADER_INFO = BColors.OKBLUE + "NODE GENERATOR:" + BColors.ENDC
_MSG_HEADER_FAIL = BColors.FAIL + "NODE GENERATOR - ERROR:" + BColors.ENDC
_MSG_HEADER_SUCCESS = BColors.OKGREEN + "NODE GENERATOR - SUCCESS:" + BColors.ENDC


class NodeGenerator(BackendGenerator):
    def __init__(self, model, builtins, path):
        super(NodeGenerator, self).__init__(model, builtins, path)
        self.base_url = "http://localhost:3000/"
        self.app_name = "genan_node"
        self.objects = []
        path = os.path.abspath(__file__)
        module_path = os.path.dirname(path)
        with open(os.path.join(module_path, 'config.json')) as data_file:
            self.type_mapper = json.load(data_file)

    def generate(self):
        print(_MSG_HEADER_INFO + " Started.")
        app_name = input(_MSG_HEADER_INFO + " Name of your application (default: genan_node): ")

        if app_name and app_name == "":
            self.app_name = app_name

        try:
            base_path = os.path.join(self.path, self.app_name)
            if not os.path.exists(base_path):
                os.makedirs(base_path)

            subprocess.check_call(["express"], cwd=base_path)
            print(_MSG_HEADER_INFO + " Installing dependencies...")

            subprocess.check_call(["npm", "install"], cwd=base_path)
            subprocess.check_call(["npm", "install", "mongoose", "--save"],
                                  cwd=base_path)
            subprocess.check_call(["npm", "install", "lodash", "--save"],
                                  cwd=base_path)
            subprocess.check_call(["npm", "install", "debug", "--save"],
                                  cwd=base_path)
            subprocess.check_call(["npm", "install", "cors", "--save"],
                                      cwd=base_path)

            print(_MSG_HEADER_INFO + "Removing unnecesarry Express Generator's generated files.")

            subprocess.check_call(["rm", "routes/users.js"], cwd = base_path)
            subprocess.check_call(["rm", "routes/index.js"], cwd = base_path)
            subprocess.check_call(["rm", "-rf", "views"], cwd = base_path)

            print(_MSG_HEADER_INFO + " Generating backend...")
            for concept in self.model.concept:
                if hasattr(concept, 'accept'):
                    obj = concept.accept(self)
                    if obj:
                        self.objects.append(obj)

            render_app = get_template("app.js", objects=self.objects, app_name=self.app_name)
            app_file = open(os.path.join(self.path, self.app_name, "app.js"), "w+")
            path = os.path.abspath(__file__)
            module_path = os.path.dirname(path)
            shutil.copy(os.path.join(module_path, "templates", "common.js"),
                        os.path.join(self.path, self.app_name))
            print(render_app, file=app_file)

            print(_MSG_HEADER_SUCCESS + " Finished the backend generation.")
        except subprocess.CalledProcessError as e:
            print(_MSG_HEADER_FAIL + " (NPM ERROR): " + str(e))
            print(_MSG_HEADER_FAIL + " Unable to generate the backend. Cleaning up...")
            shutil.rmtree(base_path)
            raise e
        except Exception as e:
            print(_MSG_HEADER_FAIL + str(e))
            print(_MSG_HEADER_FAIL + " Unable to generate the backend. Cleaning up...")
            shutil.rmtree(base_path)
            raise e

    def visit_object(self, object):
        """
        generate_object(self, object)
        Generates a node.js RESTful service, routes, their default and customizable callbacks and models for an object.
        :param object:
        :return object:
        """

        base_path = os.path.join(self.path, self.app_name)


        generate_component(object, "model", "model.js", base_path, "models", persistent_types = self.type_mapper)
        generate_component(object, "route", "route.js", base_path, "routes")
        generate_component(object, "default route callbacks", "default_route_callbacks.js", base_path, "routes", ".default_route_callbacks")
        generate_component(object, "overridable route callbacks", "route_callbacks.js", base_path, "routes", "route_callbacks")

        return object


def generate_component(object, component_name, template_name, base_path, *args, **kwargs):
    """
        Generates an Express API component from its template and places it in joined base_path and args path
    """
    print(_MSG_HEADER_INFO + "Generating {0} for {1}".format(component_name, object.name))
    route_callbacks_path = os.path.join(base_path, *args)
    rendered_route_callbacks = get_template(template_name, o = object, **kwargs)
    if not os.path.exists(route_callbacks_path):
        os.makedirs(route_callbacks_path)
    file_route_callbacks = open(os.path.join(route_callbacks_path, "{0}_{1}".format(object.name, template_name)), 'w+')
    print(rendered_route_callbacks, file = file_route_callbacks)

def get_template(template_name, **kwargs):
    """
    get_template(template_name, **kwargs)
    Gets template under generation/templates folder and its subfolders.
    Takes additional parameters required for the template to be rendered.
    """
    path = os.path.abspath(__file__)
    module_path = os.path.dirname(path)
    env = Environment(trim_blocks=True, lstrip_blocks=True,
                      loader=FileSystemLoader(os.path.join(module_path, "templates"), ))
    env.filters['sub_routes'] = sub_routes_filter
    env.filters['router_var'] = router_var
    env.filters['unique_types'] = unique_types
    template = env.get_template("{0}".format(template_name))
    return template.render(kwargs)
