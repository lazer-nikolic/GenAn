import traceback

import os

import pelix.framework
from pelix.ipopo.decorators import ComponentFactory, Provides, Requires, Instantiate, Validate
import logging

from interpretation.interpreter import Interpreter

# @click.command()
# @click.option('-h', '--help', is_flag=True, help='Help.')
# @click.argument('src', nargs=1, type=click.Path(exists=True))
# @click.argument('dest', nargs=1, type=click.Path(exists=True))
# def main(src, dest, help):
from main.common import BColors


@ComponentFactory("genan_core")
@Provides("spell_checker_service")
@Requires("_frontend_generator", "genan_frontend_generator")
@Requires("_backend_generator", "genan_backend_generator")
@Instantiate("genan_core")
class GenanCore(object):
    def __init__(self):
        self._backend_generator = None
        self._frontend_generator = None

        input_path = "../../test/example.gn"
        output_path = "../../gen_test/"

        self.output_file = os.path.join(os.path.dirname(output_path))

        file_path = os.path.join(input_path)
        print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Loading model from file {0}".format(file_path))

        interpreter = Interpreter()
        self.model = interpreter.load_model(file_path)
        self.builtins = interpreter.builtins

    @Validate
    def validate(self, context):

        print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Running GenAn...")

        self.generate(True)
        print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Done.")

    def generate(self, debug=False):
        try:
            if self._backend_generator:
                self.init_generator(self._backend_generator)
                self._backend_generator.generate()
            if self._frontend_generator:
                if self._backend_generator.base_url:
                    self._frontend_generator.backend_base_url = self._backend_generator.base_url
                self.init_generator(self._frontend_generator)
                self._frontend_generator.generate()
        except Exception as e:
            print(BColors.FAIL + "ERROR:" + BColors.FAIL)
            if debug:
                traceback.print_tb(e.__traceback__)
            print(BColors.FAIL + "ERROR:" + BColors.ENDC + " Generation failed.")

    def init_generator(self, generator):
        if generator:
            generator.model = self.model
            generator.builtins = self.builtins
            generator.path = self.output_file


def main():
    """
    Starts a Pelix framework and waits for it to stop
    """
    framework = pelix.framework.create_framework((
        "pelix.ipopo.core",
        "pelix.shell.core",))

    framework.start()

    context = framework.get_bundle_context()

    context.install_bundle("node_generator", "../node_gen/").start()
    context.install_bundle("angular_generator", "../angular_gen/").start()

    context.install_bundle("genan").start()

    framework.wait_for_stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
