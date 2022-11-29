#class 2 methods 1. to set the mapping, and 2 to get the maps. retturn self.method_amp.
# register students based on their score. then 

class RewardMap:

    rewardmap = None

    @classmethod
    def register(cls, grade, operation):
        
        if cls.rewardmap == None:
            cls.rewardmap = {}

        cls.rewardmap[grade] = operation

    @classmethod
    def get_register(cls):

        if cls.rewardmap == None:
            cls.rewardmap = {}

        return cls.rewardmap