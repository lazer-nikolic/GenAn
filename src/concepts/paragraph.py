'''
Created on 08.02.2016.

@author: Lazar
'''

class Paragraph(object):
    '''
    classdocs
    '''

    def __init__(self, parent, paragraph):
        self.parent = parent
        self.paragraph = paragraph

    def accept(self, visitor):
        return visitor.visit_other_selector("paragraph", paragrpah=self.paragraph)
