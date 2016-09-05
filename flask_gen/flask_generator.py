import json
import subprocess

import os
import shutil

import datetime

from angular_gen.jinja_filters import sub_routes_filter
from jinja2 import FileSystemLoader, Environment
from main.common import BColors, BackendGenerator

_MSG_HEADER_INFO = BColors.OKBLUE + "FLASK GENERATOR:" + BColors.ENDC
_MSG_HEADER_FAIL = BColors.FAIL + "FLASK GENERATOR - ERROR:" + BColors.ENDC
_MSG_HEADER_SUCCESS = BColors.OKGREEN + "FLASK GENERATOR - SUCCESS:" + BColors.ENDC


class FlaskGenerator(BackendGenerator):
    def __init__(self, model, builtins, path):
        super(FlaskGenerator, self).__init__(model, builtins, path)
        self.base_url = "http://localhost:5000/"
        self.app_name = "genan_flask"
        self.objects = []
        path = os.path.abspath(__file__)
        module_path = os.path.dirname(path)
        with open(os.path.join(module_path, 'config.json')) as data_file:
            self.type_mapper = json.load(data_file)

    def generate(self):
        print(_MSG_HEADER_INFO + " Started.")
        app_name = input(_MSG_HEADER_INFO + " Name of your application (default: genan_flask): ")

        if app_name and app_name == "":
            self.app_name = app_name

        try:
            base_path = os.path.join(self.path, self.app_name)
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            if not os.path.exists(os.path.join(base_path, "app")):
                os.makedirs(os.path.join(base_path, "app"))

            print(_MSG_HEADER_INFO + " Generating backend...")
            for concept in self.model.concept:
                if hasattr(concept, 'accept'):
                    obj = concept.accept(self)
                    if obj:
                        self.objects.append(obj)

            # Generate __init__.py, config.jinja and run.py
            render_file = get_template("app.jinja", objects=self.objects)
            target_file = open(os.path.join(base_path, "app", "__init__.py"), "w+")
            print(render_file, file=target_file)

            render_file = get_template("config.jinja")
            target_file = open(os.path.join(base_path, "config.py"), "w+")
            print(render_file, file=target_file)

            render_file = get_template("run.jinja", objects=self.objects)
            target_file = open(os.path.join(base_path, "run.py"), "w+")
            print(render_file, file=target_file)

            # Make user_code folder for hand written code
            user_code_path = os.path.join(base_path, 'user_code')
            if not os.path.exists(user_code_path):
                os.makedirs(user_code_path)
                # __init__ file should contain all hand written applications (mods)
                # Loads all fields of type Blueprint
                if not os.path.exists(os.path.join(user_code_path, "__init__.py")):
                    init_file = open(os.path.join(user_code_path, "__init__.py"), "w+")
                    print("# Import all Blueprint modules here", file=init_file)

            print(_MSG_HEADER_SUCCESS + " Finished the backend generation.")
        except Exception as e:
            print(_MSG_HEADER_FAIL + str(e))
            print(_MSG_HEADER_FAIL + " Unable to generate the backend. Cleaning up...")
            shutil.rmtree(base_path)
            raise e

    def visit_object(self, object):
        """
        generate_object(self, object)
        Generates a module containing models and views for an object.
        :param object:
        :return:
        """
        print(_MSG_HEADER_INFO + " Generating module for {0}".format(object.name))
        base_path = os.path.join(self.path, self.app_name)

        # Generate models.py
        print(_MSG_HEADER_INFO + " Generating models for {0}".format(object.name))
        module_path = os.path.join(base_path, "app", object.name)
        rendered_model = get_template("model.jinja", o=object, persistent_types=self.type_mapper)
        if not os.path.exists(module_path):
            os.makedirs(module_path)
        file_model = open(os.path.join(module_path, "models.py"), 'w+')
        print(rendered_model, file=file_model)

        # Generate views.py
        print(_MSG_HEADER_INFO + " Generating views for {0}".format(object.name))
        rendered_rest = get_template("view.jinja", o=object)
        file_rest = open(os.path.join(module_path, "views.py"), 'w+')
        print(rendered_rest, file=file_rest)

        # Generate __init__.py
        package_file = open(os.path.join(module_path, "__init__.py"), 'w+')
        print('', file=package_file)
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
    template = env.get_template("{0}".format(template_name))
    # Add current date for date of generation
    kwargs['date'] = datetime.datetime.now()
    return template.render(kwargs)
