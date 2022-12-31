
import pdb

def fever_checker(func_object):

    def wrapper(*args):
        
        name,temp = func_object(*args

        if temp >= 37.5:
            print(f'{name} has fever...')
        else:
            print(f'{name} donot have fever...')

    return wrapper


@fever_checker
def person(name: str, temp:float):
    
    print("please wait..... checking for fever......")
    return name, temp

# call
person("gowtham", 40)
