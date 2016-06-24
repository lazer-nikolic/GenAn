'''
Created on 08.02.2016.

@author: Lazar
'''

from textx.exceptions import TextXSemanticError

def jumbo_procesor(object):
   
    for x in object.jumbo:
        if x.heading !='':
            if not object.heading is None:
                raise TextXSemanticError("You can't use more than one heading attribute.")
            object.heading = x.heading
        elif x.text !='':
            if not object.text is None:
                raise TextXSemanticError("You can't use more than one text attribute.")
            object.text = x.text
        elif x.imgPath !='':
            if not object.imgPath is None:
                raise TextXSemanticError("You can't use more than one imgPath attribute.")
            object.imgPath = x.imgPath
        elif not x.ref is None:
            if not object.ref is None:
                raise TextXSemanticError("You can't use more than one ref keyword.")
            object.ref = x.ref
            

class Jumbo(object):
    '''
    classdocs
    '''

    def __init__(self, parent, jumbo):
        self.parent = parent
        self.type = type
        self.jumbo = jumbo
        self.heading = None
        self.text = None
        self.ref = None
        self.imgPath = None

    def accept(self, visitor):
        return visitor.visit_other_selector("jumbo", jumbo=self)
