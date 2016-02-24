from generation.generator import Generator
from interpretation.interpreter import Interpreter
from main import genan


def test_auto_init():
    """
    Test that attributes are initialized to propper
    values if not specified in the model.
    """

    interpreter = Interpreter()
    model = interpreter.load_model("test.gn")

    generator = Generator(model, interpreter.builtins, "")
    generator.generate()