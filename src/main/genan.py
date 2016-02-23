import os
from generation.generator import Generator, BColors
from interpretation.interpreter import Interpreter

if __name__ == "__main__":
    print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Running GenAn...")

    output_file = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'gen_test')

    this_dir = os.path.dirname(__file__)
    file_path = os.path.join(this_dir, os.pardir, os.pardir, 'test', 'test.gn')
    print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Loading model from file {0}".format(file_path))
    interpreter = Interpreter()
    model = interpreter.load_model(file_path)

    generator = Generator(model, interpreter.builtins, output_file)
    generator.generate()
    print(BColors.OKBLUE + "GENAN:" + BColors.ENDC + " Done.")