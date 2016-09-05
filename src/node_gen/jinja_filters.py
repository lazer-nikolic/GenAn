
def router_var(resource):
    return resource.lower() + 'Router'

def unique_types(relations):
    ''' 
        Returns a list of unique types of related entities
        (makes list of unique elements if there are more
         than one relation between two entities)
    '''
    types = [ relation.object.name for relation in relations]
    return list(set(types)) 
