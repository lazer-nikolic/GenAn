'''
Created on 08.02.2016.

@author: Lazar
'''
from generation.generator import BColors


def view_in_view_processor(view_in_view):
    line, col = view_in_view._tx_metamodel.parser.pos_to_linecol(
                view_in_view._tx_position)

    if view_in_view.position:
        if view_in_view.position > 12:
            print(BColors.WARNING + "WARNING: " + BColors.ENDC +
                  "(at %d, %d) Position %d must be a number in 1-12 range." %
                  (line, col, view_in_view.position))
        elif view_in_view.position < 1:
            print(BColors.WARNING + "WARNING: " + BColors.ENDC +
                  "(at %d, %d) Position %d must be a number in 1-12 range." %
                  (line, col, view_in_view.position))
    if view_in_view.size:
        if view_in_view.size > 12:
            print(BColors.WARNING + "WARNING: " + BColors.ENDC +
                  "(at %d, %d) Size %d must be a number in 1-12 range." %
                  (line, col, view_in_view.size))
        elif view_in_view.size < 1:
            print(BColors.WARNING + "WARNING: " + BColors.ENDC +
                  "(at %d, %d) Size %d must be a number in 1-12 range." %
                  (line, col, view_in_view.position))
        if view_in_view.position:
            if 12 - view_in_view.position < view_in_view.size:
                print(BColors.WARNING + "WARNING: " + BColors.ENDC +
                      "(at %d, %d) Size %d of component exceeds row size on position %d." %
                      (line, col, view_in_view.size, view_in_view.position))


class ViewInView(object):
    '''
    classdocs
    '''

    def __init__(self, selector, parent, position=1, size=0):
        self.selector = selector
        self.position = position
        self.size = size
        self.parent = parent
