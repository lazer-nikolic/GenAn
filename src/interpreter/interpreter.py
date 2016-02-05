'''
Created on 03.02.2016.

@author: Lazar
'''
from textx.metamodel import metamodel_from_file
    
class View:
    basic_type_names = ['text', 'number', 'check', 'option', 'link', 'ref', 'email', 'password', 'menuitem', 'menu', 'button', 'radio', 'form', 'label', 'image']
    
    def __init__(self, parent, name, views):
        self.name = name
        self.views = views
        self.parent = parent

    def __str__(self):
        return self.name


if __name__ == "__main__":
    
    basic_types = {x : View(None,x, []) for x in View.basic_type_names}
    
    my_mm = metamodel_from_file('../grammar/grammar.tx',
                                 classes = [View],
                                 builtins = basic_types,
                                 debug = False)
    
    # Create model
    my_model = my_mm.model_from_file('../../test/test.gn')