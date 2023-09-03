import math 



def convert_to_snake_case(string):
    return string.replace(' ', '_').lower() 


def get_album(album1, album2):
    try:
        if math.isnan(album2):
            return album1
        else:
            return album2
    except:
        return album2