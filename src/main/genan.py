import os
from generation.generator import Generator
from interpretation.interpreter import Interpreter

if __name__ == "__main__":
    print("Running GenAn...")

    output_file = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'gen_test')

    this_dir = os.path.dirname(__file__)
    file_path = os.path.join(this_dir, os.pardir, os.pardir, 'test', 'test.gn')

    interpreter = Interpreter()
    model = interpreter.load_model(file_path)

    generator = Generator(model, interpreter.builtins, output_file)
    generator.generate()


# if __name__ == "__main__":
#     parser = OptionParser()
#     parser.add_option("-o", "--output", dest="output_file",
#                       help="generate to OUTPUT", metavar="OUTPUT")
#
#     (options, args) = parser.parse_args()
#     option_dict = vars(options)
#     main(option_dict['output_file'])