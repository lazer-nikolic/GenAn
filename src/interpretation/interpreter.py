'''
Created on 03.02.2016.

@author: Lazar
'''
import os
from concepts.layout import Layout
from concepts.object import Object
from concepts.page import page_processor
from concepts.property import Property
from concepts.selector_object import SelectorObject, selector_object_processor
from concepts.selector_view import SelectorView
from concepts.view import View
from generation.generator import Generator
from textx.metamodel import metamodel_from_file

if __name__ == "__main__":
    builtins = {x: View(None, x, []) for x in View.basic_type_names}
    layouts = {
        'border': Layout('border', ['top', 'bottom', 'center',
                                    'left', 'right'], None),
        'grid': Layout('grid', [], None)
    }

    builtins.update(layouts)

    obj_processors = {
        'SelectorObject': selector_object_processor,
        'Page': page_processor
    }

    this_dir = os.path.dirname(__file__)
    my_mm = metamodel_from_file(os.path.join(this_dir,
                                             '..', 'grammar', 'grammar.tx'),
                                classes=[
                                    View,
                                    Object,
                                    Property,
                                    SelectorObject,
                                    SelectorView
                                ],
                                builtins=builtins,
                                debug=False)

    my_mm.register_obj_processors(obj_processors)
    # Create model
    my_model = my_mm.model_from_file(os.path.join(this_dir,
                                                  '..', '..',
                                                  'test', 'test.gn'))
    print(my_model.concept)

    generator = Generator(my_model, builtins, '')
    generator.generate()
