'''
Created on 08.02.2016.

@author: Lazar
'''
def static_link_procesor(object):
    classesString = "";
    if not object.classes is None:
        for x in object.classes.htmlClasses:
            if hasattr(x, 'value'):
                classesString += " " + x.key + "=\"" + x.value + "\"";
            else:
                classesString += " " + x.key;
        object.classes = classesString
    else:
        object.classes = ""
    
    object.classes=classesString

class StaticLink(object):
    '''
    classdocs
    '''

    def __init__(self, parent, stLink, classes):
        self.parent = parent
        self.stLink = stLink
        self.classes =classes
        
