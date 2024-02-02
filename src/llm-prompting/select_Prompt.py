

def read_specific_line(filename: str, line_number: int) -> str:
    """
    Reads a specific line from a given file.

    :param filename: The path to the file.
    :param line_number: The line number to read (1-indexed).
    :return: The content of the specified line, stripped of leading/trailing whitespace.
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        # Adjusting line_number to 0-indexed by subtracting 1
        selected_line = lines[line_number - 1].strip()
        
        # Optionally print the line (you can remove this print statement if not needed)
       # print(selected_line)
        
        return selected_line
    except IndexError:
        print(f"Error: The file does not have a line {line_number}.")
        return ""
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""
    
#line_content = read_specific_line('treePromptVersion0.json', 10)
#print(f"line_content = {line_content}")