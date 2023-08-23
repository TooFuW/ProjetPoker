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

def list_lobbys_convert_str(liste : list):
    for list_lobby in liste:
        try:
            list_lobby[0] = int(list_lobby[0])
            list_lobby[2] = int(list_lobby[2])
            list_lobby[3] = int(list_lobby[3])
            list_lobby[4] = str_to_bool(list_lobby[4])
            list_lobby[6] = int(list_lobby[6])
        except:
            raise TypeError

def str_to_bool(string : str):
    return string.lstrip() == "True"