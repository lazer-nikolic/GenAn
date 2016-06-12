import traceback

import os
from angular_gen.angular_generator import AngularGenerator
from generation.generator import generate
from interpretation.interpreter import Interpreter
from node_gen.node_generator import NodeGenerator

# @click.command()
# @click.option('-h', '--help', is_flag=True, help='Help.')
# @click.argument('src', nargs=1, type=click.Path(exists=True))
# @click.argument('dest', nargs=1, type=click.Path(exists=True))
# def main(src, dest, help):
from main.common import BColors


def main():
    input_path = "../../test/example.gn"
    output_path = "../../gen_test/"

    print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Running GenAn...")

    output_file = os.path.join(os.path.dirname(output_path))

    file_path = os.path.join(input_path)
    print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Loading model from file {0}".format(file_path))
    interpreter = Interpreter()
    model = interpreter.load_model(file_path)

    frontend_generator = AngularGenerator(model, interpreter.builtins, output_file)

    backend_generator = NodeGenerator(model, interpreter.builtins, output_file)

    generate(frontend_generator, backend_generator, True)
    print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Done.")


def generate(frontend_generator, backend_generator=None, debug=False):
    try:
        if backend_generator:
            backend_generator.generate()
        if frontend_generator:
            if backend_generator.base_url:
                frontend_generator.backend_base_url = backend_generator.base_url
            frontend_generator.generate()
    except Exception as e:
        print(BColors.FAIL + "ERROR:" + BColors.FAIL)
        if debug:
            traceback.print_tb(e.__traceback__)
        print(BColors.FAIL + "ERROR:" + BColors.ENDC + " Generation failed.")


if __name__ == '__main__':
    main()
