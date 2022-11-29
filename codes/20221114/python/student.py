from beginningregister import LayerMap


class Student:
    
    def __init__(self, name:str, grade:str, year:int, department:str):

        self.name = name
        self.grade = grade
        self.year = year
        self.department = department

    def reward(self):
        layermap = LayerMap.get_register()
        return layermap[self.grade]() #calls the functions and calculates the reward
        # Now if this wasn't the case then I would have to check if self.grade is "A" or "B" or "C" and the add condition for that
