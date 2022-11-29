#add to map
from beginningregister import RewardMap

def register_layer(grade):
    
    def add_to_map(method):
        
        RewardMap.register(grade, method)

    
    return add_to_map