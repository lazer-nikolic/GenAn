'''
Created on 08.02.2016.

@author: Lazar
'''


def view_on_page_processor(view_on_page):
    selector = view_on_page.selector
    if hasattr(selector, 'view'):
        builtins = view_on_page._tx_metamodel.builtins
        view_name = selector.view.name
        view = selector.view
        if view_name not in builtins:
            view_on_page.parent.subviews.append(view)

class ViewOnPage(object):
    '''
    classdocs
    '''

    def __init__(self, position, parent, selector):
        self.position = position
        self.parent = parent
        self.selector = selector
