import json
import subprocess

import os
import shutil

from pelix.ipopo.decorators import ComponentFactory, Instantiate, Property, Provides

from angular_gen.jinja_filters import sub_routes_filter
from jinja2 import FileSystemLoader, Environment

from main.common import BColors, BackendGenerator

_MSG_HEADER_INFO = BColors.OKBLUE + "NODE GENERATOR:" + BColors.ENDC
_MSG_HEADER_FAIL = BColors.FAIL + "NODE GENERATOR - ERROR:" + BColors.ENDC
_MSG_HEADER_SUCCESS = BColors.OKGREEN + "NODE GENERATOR - SUCCESS:" + BColors.ENDC


@ComponentFactory("genan_node_generator_factory")
@Provides("genan_backend_generator")
@Property("_name", "name", "genan_nodejs")
@Instantiate("genan_node_generator")
class NodeGenerator(BackendGenerator):
    def __init__(self):
        super(NodeGenerator, self).__init__()
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

            yes = ['yes', 'y', 'Y', 'Yes', 'YES', '']

            choice_npm = input(_MSG_HEADER_INFO + " Install npm [y/n] (default: yes): ")
            if choice_npm in yes:
                subprocess.check_call(["npm", "install"], cwd=base_path)
                subprocess.check_call(["npm", "install", "mongoose", "--save"],
                                      cwd=base_path)
                subprocess.check_call(["npm", "install", "ejs", "--save"],
                                      cwd=base_path)
                subprocess.check_call(["npm", "install", "debug", "--save"],
                                      cwd=base_path)
                subprocess.check_call(["npm", "install", "cors", "--save"],
                                      cwd=base_path)

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
        Generates a node.js rest service, route and model for an object.
        :param object:
        :return:
        """

        base_path = os.path.join(self.path, self.app_name)

        print(_MSG_HEADER_INFO + " Generating model for {0}".format(object.name))
        models_path = os.path.join(base_path, "models")
        rendered_model = get_template("model.js", o=object, persistent_types=self.type_mapper)
        if not os.path.exists(models_path):
            os.makedirs(models_path)
        file_model = open(os.path.join(models_path, "{0}.js".format(object.name)), 'w+')
        print(rendered_model, file=file_model)

        print(_MSG_HEADER_INFO + " Generating service for {0}".format(object.name))
        routes_path = os.path.join(base_path, "routes")
        rendered_rest = get_template("rest.js", o=object)
        if not os.path.exists(routes_path):
            os.makedirs(routes_path)
        file_rest = open(os.path.join(routes_path, "{0}.js".format(object.name)), 'w+')
        print(rendered_rest, file=file_rest)

        return object


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
    template = env.get_template("{0}".format(template_name))
    return template.render(kwargs)
