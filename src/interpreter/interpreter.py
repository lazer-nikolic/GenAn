'''
Created on 03.02.2016.

@author: Lazar
'''
from textx.metamodel import metamodel_from_file

from concepts.object import Object
from concepts.property import Property
from concepts.selector_object import SelectorObject, selector_object_processor
from concepts.selector_view import SelectorView
from concepts.view import View


if __name__ == "__main__":
    
    basic_types = {x : View(None,x, []) for x in View.basic_type_names}
    
    obj_processors = {
                      'SelectorObject' : selector_object_processor
                      }
    
    my_mm = metamodel_from_file('../grammar/grammar.tx',
                                 classes = [
                                            View, 
                                            Object, 
                                            Property, 
                                            SelectorObject, 
                                            SelectorView
                                            ],
                                 builtins = basic_types,
                                 debug = False)
    
    my_mm.register_obj_processors(obj_processors)
    # Create model
    my_model = my_mm.model_from_file('../../test/test.gn')
    my_model
    