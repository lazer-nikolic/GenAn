'''
Created on 03.02.2016.

@author: Lazar
'''
import os
from concepts.layout import Layout
from concepts.menu import Menu
from concepts.menubar import Menubar
from concepts.object import Object
from concepts.page import page_processor, Page
from concepts.property import Property, property_processor
from concepts.row import Row
from concepts.row_separator import RowSeparator
from concepts.selector_object import SelectorObject, selector_object_processor
from concepts.selector_view import SelectorView
from concepts.sidebar import Sidebar
from concepts.view import View
from concepts.data_show import DataShow, data_show_processor
from concepts.form import Form
from concepts.view_in_view import ViewInView, view_in_view_processor
from concepts.view_on_page import ViewOnPage, view_on_page_processor
from concepts.ref_link import RefLink, ref_link_procesor
from concepts.footer import Footer
from concepts.use import Use
from concepts.jumbo import Jumbo, jumbo_procesor
from concepts.jumbo_parameters import JumboParameters
from concepts.object import object_processor
from concepts.paragraph import Paragraph
from concepts.static_link import StaticLink, static_link_procesor
from concepts.addition_parameters import AdditionParameters
from concepts.query import Query, query_processor
from concepts.string_condition import StringCondition
from concepts.integer_condition import IntegerCondition
from textx.metamodel import metamodel_from_file


class Interpreter:
    def __init__(self):
        builtins = {x: View(None, x, []) for x in View.basic_type_names}
        layouts = {
            'border': Layout('border', ['top', 'center',
                                        'left', 'right', 'bottom'], None),
            'grid': Layout('grid', [], None)
        }

        builtins.update(layouts)

        self.grammar_path = os.path.join(os.pardir, 'grammar', 'grammar.tx')
        self.builtins = builtins
        self.obj_processors = {
            'SelectorObject': selector_object_processor,
            'Page': page_processor,
            'Property': property_processor,
            'DataShow': data_show_processor,
            'RefLink': ref_link_procesor,
            'ViewInView': view_in_view_processor,
            'Jumbo': jumbo_procesor,
            'Query': query_processor,
            'StaticLink': static_link_procesor,
            'ViewOnPage': view_on_page_processor,
            'Object':object_processor
        }

    def load_model(self, file_path):
        # Create model
        meta_model = metamodel_from_file(self.grammar_path,
                                         classes=[
                                             View,
                                             Object,
                                             Page,
                                             Property,
                                             Query,
                                             StringCondition,
                                             IntegerCondition,
                                             SelectorObject,
                                             SelectorView,
                                             ViewOnPage,
                                             DataShow,
                                             Sidebar,
                                             Layout,
                                             Menubar,
                                             Menu,
                                             Form,
                                             RefLink,
                                             Footer,
                                             Use,
                                             Row,
                                             ViewInView,
                                             RowSeparator,
                                             AdditionParameters,
                                             Paragraph,
                                             Jumbo,
                                             JumboParameters,
                                             AdditionParameters,
                                             StaticLink
                                         ],
                                         builtins=self.builtins,
                                         debug=False)

        meta_model.register_obj_processors(self.obj_processors)

        return meta_model.model_from_file(file_path)
