import word
import random

left_list, right_list = word.r_word()
all_includes = []

def init():
    for i in range(len(left_list)):
        all_includes.append(i)
    random.shuffle(all_includes)
    return all_includes
    
def left(i):
    try:
        global all_includes, left_list
        
        return left_list[all_includes[i]]
    except:
        return 0
    
def right(i, answer):
    try:
        global right_list, all_includes
        if str(right_list[all_includes[i]]) == str(answer):
            return 1
        else:
            return 0
    except:
        return 0