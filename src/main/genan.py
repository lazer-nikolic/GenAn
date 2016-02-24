import argparse

import os
from generation.generator import Generator, BColors
from interpretation.interpreter import Interpreter

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('input', metavar='input', help='input file')
    parser.add_argument('output', default='', metavar='output', help='output file', nargs='?')
    args = parser.parse_args()
    print(args)

    input_path = args.input
    output_path = args.output

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
