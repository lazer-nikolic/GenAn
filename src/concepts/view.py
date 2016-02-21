'''
Created on 08.02.2016.

@author: Lazar
'''
from concepts.row import Row


class View(object):

    basic_type_names = ['text', 'number', 'checkbox', 'link', 
                        'email', 'password', 'menuitem', 'menu',
                        'button', 'radio', 'form', 'label', 'image', 
                        'date', 'combobox', 'list', 'table',
                        'thumbnail', "row"]

    def __init__(self, parent, name, views):
        self.name = name
        self.views = views
        self.parent = parent
        self.rows = []

        row_selectors = []
        for view_selector in views:
            if view_selector.__class__.__name__ == 'RowSeparator':
                self.rows.append(Row(row_selectors, self))
                row_selectors.clear()
            else:
                row_selectors.append(view_selector)
        if row_selectors:
            self.rows.append(Row(row_selectors, self))
            row_selectors.clear()

    def __str__(self):
        return self.name
