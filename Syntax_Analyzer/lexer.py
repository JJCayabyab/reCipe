import os
from lexer import LexicalAnalyzer

def open_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def save_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"File saved to {file_path}")
        return True
    except Exception as e:
        print(f"Failed to save file: {e}")
        return False

def analyze_code(input_program):
    lexer = LexicalAnalyzer()
    tokens = lexer.tokenize(input_program)
    
    result = []

    # Format tokens for display
    for lexeme, token in tokens:
        result.append(f"{lexeme} |\t{token}")

    return result


def download_output(file_name, output_content):
    if not output_content:
        print("There is no output to download!")
        return False

    try:
        with open(file_name, "w") as output_file:
            output_file.write("Lexeme | Token\n")  
            for result in output_content:
                output_file.write(result + '\n')
        print(f"Output saved to {file_name}")
        return True
    except Exception as e:
        print(f"Failed to save output: {e}")
        return False

# Specify the directory path
directory_path = r"C:\Users\Josh\Documents\VSCODE python\PARSER-FINAL"

if os.path.exists(directory_path):
    # Loop through files with ".ck" extension in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".up"):
            file_path = os.path.join(directory_path, filename)
            print(f"Processing file: {file_path}")
            
            content = open_file(file_path)
            
            if content is not None:
                analyzed_result = analyze_code(content)
                # Use a fixed output file name "lexer.txt" for each input file
                output_file_name = "lexer.txt"
                download_output(output_file_name, analyzed_result)
else:
    print(f"The directory '{directory_path}' does not exist.")