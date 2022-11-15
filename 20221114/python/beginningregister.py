#class 2 methods 1. to set the mapping, and 2 to get the maps. retturn self.method_amp.
# register students based on their score. then 

class LayerMap:

    layermap = None

    @classmethod
    def register(cls, layername, operation):
        
        if cls.layermap == None:
            cls.layermap = {}

        cls.layermap[layername] = operation

    @classmethod
    def get_register(cls):

        if cls.layermap == None:
            cls.layermap = {}

        return cls.layermap