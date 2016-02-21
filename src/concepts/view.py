'''
Created on 08.02.2016.

@author: Lazar
'''
from concepts.row import Row
from textx.exceptions import TextXSemanticError

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

        seen = set()

        row = Row(self, 1)
        last_row_number = 1
        for view_selector in views:
            if view_selector.__class__.__name__ == 'RowSeparator':
                if view_selector.number < 0:
                    row_number = last_row_number
                    last_row_number += 1
                else:
                    if view_selector.number and view_selector.number not in seen:
                        seen.add(view_selector.number)
                    else:
                        line, col = self._tx_metamodel.parser.pos_to_linecol(self._tx_position)
                        raise TextXSemanticError("ERROR: (at %d, %d) More than one row at position %d." %
                                                 (line, col, view_selector.number))
                    last_row_number = view_selector.number
                    row_number = view_selector.number
                self.rows.append(row)
                row = Row(self, row_number)
            else:
                row.selectors.append(view_selector)
        if row not in self.rows:
            self.rows.append(row)

    def __str__(self):
        return self.name
