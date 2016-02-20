'''
Created on 08.02.2016.

@author: Lazar
'''
def ref_link_procesor(ref_link):
    if not ref_link.ref is None:
        ref_link.ref = ref_link.ref.page.name
    else:
        ref_link.ref = ref_link.aps_ref

class RefLink(object):
    '''
    classdocs
    '''

    def __init__(self, label, ref, parent, aps_ref):
        self.label = label
        self.ref = ref
        self.parent = parent
        self.aps_ref = aps_ref
