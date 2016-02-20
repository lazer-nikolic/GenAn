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
        page.layout = Layout('border', ['top', 'bottom', 'center', 'left', 'right'], None)

    for view_on_page in page.views:
        if not view_on_page.position in page.layout.positions:
            raise TextXSemanticError(
                    "Position '{0}' is not supported by {1} layout".format(view_on_page.position, page.layout.name))


class Page(object):
    '''
    classdocs
    '''

    def __init__(self, name, title, views, parent, layout, sidebar, menubar):
        self.name = name
        self.title = title
        self.views = views
        self.layout = layout
        self.sidebar = sidebar
        self.parent = parent
        self.menubar = menubar
