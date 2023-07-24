def str_to_list(string: str):   #fonctionne seulement sur une liste supposée valide
    liste = []
    string = string.removeprefix("[")
    string = string.removesuffix("]")

    return string.split(",")

def str_to_lists_in_list(string : str):
    current_list = []
    current_string = ""
    string = string[1:-1]
    append = False
    for i in string:
        if i == "[":
            append = True
        if i == "]":
            append = False
            current_string += i
            current_list.append(str_to_list(current_string))
            current_string = ""

        if append:
            current_string += i
    return current_list

    
