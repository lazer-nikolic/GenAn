'''
Created on 08.02.2016.

@author: Lazar
'''
from concepts.sidebar import Sidebar
from textx.exceptions import TextXSemanticError

from concepts import view_on_page
from concepts.layout import Layout

def page_processor(page):
    # Default layout je border
    if not page.layout:
        page.layout = Layout('border', ['top', 'center', 'left', 'right', 'bottom'], None)

    for view_on_page in page.views:
        if not view_on_page.position in page.layout.positions:
            raise TextXSemanticError(
                    "Position '{0}' is not supported by {1} layout".format(view_on_page.position, page.layout.name))
            
    adapter_page(page)

def adapter_page(page):
    '''
    Adapter method for mapping using on page fields.
    '''
    for x in page.using:
        if not x.f is None:
            if not page.footer is None:
                raise TextXSemanticError("You can't use more than one footer on page.")
            page.footer = x.f
        elif not x.m is None:
            if not page.menubar is None:
                raise TextXSemanticError("You can't use more than one menubar on page.")
            page.menubar = x.m
        elif not x.s is None:
            if not page.sidebar is None:
                raise TextXSemanticError("You can't use more than one sidebar on page.")
            page.sidebar = x.s

class Page(object):
    '''
    classdocs
    '''

    def __init__(self, name, title, views, parent, layout, using):
        self.name = name
        self.title = title
        self.views = views
        self.layout = layout
        self.parent = parent
        self.using = using
        self.footer = None
        self.menubar = None
        self.sidebar = None

