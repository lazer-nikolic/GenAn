import traceback

import os
import click

import genan_env

from angular_gen.angular_generator import AngularGenerator
from interpretation.interpreter import Interpreter
from node_gen.node_generator import NodeGenerator

from main.common import BColors

@click.command()
@click.option('--frontend', default = 'angular', 
              type = click.Choice(['angular']), 
              help = 'Generate frontend application using one of the provided Javascript frameworks.')
@click.option('--backend', default = 'node', 
              type = click.Choice(['node']), 
              help = 'Generate backend application using one of the provided technologies')
@click.argument('source_path', nargs = 1, 
                default = os.path.join(os.path.dirname(genan_env.ROOT_PATH), genan_env.TEST_DIR, 'example.gn'), 
                type = click.Path(exists = True))
@click.argument('output_path', nargs = 1, 
                default = os.path.join(os.path.dirname(genan_env.ROOT_PATH)),
                type = click.Path(exists = True))
def cli(frontend, backend, source_path, output_path):

    print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Running GenAn...")

    output_file = os.path.join(os.path.dirname(output_path))
    file_path = os.path.join(source_path)

    print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Loading model from file {0}".format(file_path))

    interpreter = Interpreter()
    model = interpreter.load_model(file_path)

    if frontend == 'angular':
        frontend_generator = AngularGenerator(model, interpreter.builtins, output_file)

    if backend == 'node':
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
    cli()
