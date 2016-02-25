import argparse

import os
from click._unicodefun import click
from generation.generator import Generator, BColors
from interpretation.interpreter import Interpreter

#@click.command()
#@click.option('-h', '--help', is_flag=True, help='Help.')
#@click.argument('src', nargs=1, type=click.Path(exists=True))
#@click.argument('dest', nargs=1, type=click.Path(exists=True))
#def main(src, dest, help):
def main():
    input_path = "../../test/example.gn"
    output_path = "../../gen_test/"

    print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Running GenAn...")

    # output_file = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'gen_test')
    output_file = os.path.join(os.path.dirname(output_path))

    this_dir = os.path.dirname(__file__)
    # file_path = os.path.join(this_dir, os.pardir, os.pardir, 'test', 'test.gn')
    file_path = os.path.join(input_path)
    print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Loading model from file {0}".format(file_path))
    interpreter = Interpreter()
    model = interpreter.load_model(file_path)

    generator = Generator(model, interpreter.builtins, output_file)
    generator.generate()
    print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Done.")

if __name__ == '__main__':
        main()
