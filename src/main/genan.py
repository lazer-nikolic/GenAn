import atexit
import importlib
import os
import re
import traceback

import pip
import pkg_resources

from interpretation.interpreter import Interpreter
from main.common import BColors


class GenanCore(object):
    def __init__(self):
        self._backend_generators = []
        self._frontend_generators = []

        # Load all .whl, .egg and .tar.gz files
        self.packages = [package_name for package_name in os.listdir(os.path.join(os.pardir, 'plugins'))
                         if re.search('^.+\.(whl|egg|tar\.gz)$', package_name)]

        atexit.register(self.cleanup)

        print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Running GenAn...")

        input_path = "../../test/example.gn"
        output_path = "../../gen_test/"

        self.output_file = os.path.join(os.path.dirname(output_path))

        file_path = os.path.join(input_path)
        print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Loading model from file {0}".format(file_path))

        interpreter = Interpreter()
        self.model = interpreter.load_model(file_path)
        self.builtins = interpreter.builtins
        self.path = output_path

        print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Loading generators...")
        self._load_plugins()

    def generate(self, debug=False):
        print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Starting generators...")
        try:
            for backend_generator in self._backend_generators:
                backend_generator.generate()
            for frontend_generator in self._frontend_generators:
                frontend_generator.backend_base_url = "http://localhost:3000"
                frontend_generator.generate()
        except Exception as e:
            print(BColors.FAIL + "ERROR:" + BColors.FAIL)
            if debug:
                traceback.print_tb(e.__traceback__)
            print(BColors.FAIL + "ERROR:" + BColors.ENDC + " Generation failed.")
        print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Done.")

    def cleanup(self):
        print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Cleaning up...")
        if self.packages:
            for package_name in self.packages:
                pip.main(["uninstall", "-y", "-q", os.path.join(os.pardir, 'plugins', package_name)])

    def _load_plugins(self):
        if self.packages:
            for package_name in self.packages:
                pip.main(["install", "-q", os.path.join(os.pardir, 'plugins', package_name)])
            # Import all installed modules
            pkg_resources._initialize_master_working_set()
        # Load frontend generators
        for entrypoint in pkg_resources.iter_entry_points("genan.frontend_generator"):
            FrontendGenerator = entrypoint.load()
            generator = FrontendGenerator(self.model, self.builtins, self.path)
            self._frontend_generators.append(generator)

        # Load backend generators
        for entrypoint in pkg_resources.iter_entry_points("genan.backend_generator"):
            BackendGenerator = entrypoint.load()
            generator = BackendGenerator(self.model, self.builtins, self.path)
            self._backend_generators.append(generator)


def main():
    try:
        generator = GenanCore()
        generator.generate(True)
    except KeyboardInterrupt:
        # Allow cleanup function to be called on forced exit
        pass


if __name__ == "__main__":
    main()
