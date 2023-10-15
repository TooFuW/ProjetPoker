import os

def count_lines_and_characters(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        line_count = len(lines)
        char_count_with_spaces = sum(len(line) for line in lines)
        char_count_without_spaces = sum(len(line.strip()) for line in lines)
    return line_count, char_count_with_spaces, char_count_without_spaces

def count_lines_and_characters_in_directory(directory, current_file):
    python_files = [f for f in os.listdir(directory) if f.endswith('.py') and f != current_file]
    
    total_lines = 0
    total_chars_with_spaces = 0
    total_chars_without_spaces = 0
    
    for file in python_files:
        file_path = os.path.join(directory, file)
        lines, chars_with_spaces, chars_without_spaces = count_lines_and_characters(file_path)
        total_lines += lines
        total_chars_with_spaces += chars_with_spaces
        total_chars_without_spaces += chars_without_spaces
    
    return total_lines, total_chars_with_spaces, total_chars_without_spaces

directory = os.path.dirname(os.path.abspath(__file__))  # Utilise le répertoire du fichier en cours
current_file = os.path.basename(__file__)  # Obtient le nom de ce fichier
total_lines, total_chars_with_spaces, total_chars_without_spaces = count_lines_and_characters_in_directory(directory, current_file)

print(f"Nombre total de lignes : {total_lines}")
print(f"Nombre total de caractères (avec espaces) : {total_chars_with_spaces}")
print(f"Nombre total de caractères (sans espaces) : {total_chars_without_spaces}")