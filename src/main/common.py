class GeneratorAdapter:
    def visit_selector_view(self, view):
        pass

    def visit_selector_object(self, object, property):
        pass

    def visit_view(self, view):
        pass

    def visit_page(self, page):
        pass

    def visit_action_selector(self, object, actions):
        pass

    def visit_other_selector(self, name, **kwargs):
        pass

    def visit_row(self, row):
        pass

    def visit_object(self, object):
        pass


class FrontendGenerator(GeneratorAdapter):
    def __init__(self, model, builtins, path):
        self.model = model
        self.builtins = builtins
        self.path = path
        self.backend_base_url = "http://localhost:8080/"


class BackendGenerator(GeneratorAdapter):
    def __init__(self, model, builtins, path):
        self.model = model
        self.builtins = builtins
        self.path = path
        self.base_url = "http://localhost:8080/"


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
