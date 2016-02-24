from generation.generator import Generator
from interpretation.interpreter import Interpreter


def test_auto_init():
    interpreter = Interpreter()
    model = interpreter.load_model("test.gn")

    generator = Generator(model, interpreter.builtins, "", True)
    generator.generate()
