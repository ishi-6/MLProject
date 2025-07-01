import re  # Regular expressions for pattern matching
import os  # Operating system functions for file handling

def load_code(file_path):
    """
    Reads the content of the input code file.
    """
    with open(file_path, 'r') as file:
        return file.read()

def remove_comments(code, language='Python'):
    """
    Removes comments from the source code based on the language.
    Supports Python and C-style comments.
    """
    if language == 'Python':
        # Remove single-line Python comments using regex
        code = re.sub(r'#.*', '', code)
    else:
        # Remove C-style single-line (//) and multi-line (/* */) comments
        code = re.sub(r'//.*', '', code)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

def normalize_spacing(code):
    """
    Normalizes spacing by removing extra spaces, tabs, and blank lines.
    """
    code = code.replace('\t', '    ')  # Replace tabs with spaces
    code = re.sub(r'[ \t]+$', '', code, flags=re.MULTILINE)  # Remove trailing spaces
    code = re.sub(r'\n\n+', '\n', code)  # Remove consecutive blank lines
    return code

def hardcoded_optimizations(code):
    """
    Applies hardcoded optimizations to known inefficient patterns in the code.
    """
    optimizations = {
        # Replace nested loops with list comprehensions where possible
        "result = []\nfor i in range(10):\n    for j in range(10):\n        result.append(i * j)":
            "result = [i * j for i in range(10) for j in range(10)]",
        
        # Optimize string concatenation inside loops with join()
        "sentence = ''\nfor word in words:\n    sentence += word + ' '":
            "sentence = ' '.join(words) + ' '",
        
        # Replace manual summation with built-in sum()
        "total = 0\nfor num in numbers:\n    total += num":
            "total = sum(numbers)",
        
        # Replace list-based uniqueness checking with set conversion
        "unique_items = []\nfor item in items:\n    if item not in unique_items:\n        unique_items.append(item)":
            "unique_items = list(set(items))"
    }
    
    for pattern, replacement in optimizations.items():
        if pattern in code:
            code = code.replace(pattern, replacement)
    
    return code

def preprocess_code(file_path, language='Python'):
    """
    Main function to preprocess the code.
    Steps:
        1. Load code from file.
        2. Remove comments.
        3. Normalize spacing.
        4. Apply hardcoded optimizations.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    code = load_code(file_path)  # Load the source code
    print("Step 1: Loaded code successfully.")

    code_no_comments = remove_comments(code, language)  # Remove comments
    print("Step 2: Removed comments.")

    cleaned_code = normalize_spacing(code_no_comments)  # Normalize spacing
    print("Step 3: Normalized spacing and formatting.")

    optimized_code = hardcoded_optimizations(cleaned_code)  # Apply optimizations
    print("Step 4: Applied hardcoded optimizations.")

    return optimized_code

def save_preprocessed_code(output_path, code):
    """
    Saves the preprocessed code to the specified output file.
    """
    with open(output_path, 'w') as file:
        file.write(code)
    print(f"Preprocessed code saved to: {output_path}")

if __name__ == '__main__':
    import argparse  # Library for parsing command-line arguments

    parser = argparse.ArgumentParser(description="Preprocess source code for analysis and optimization.")
    parser.add_argument('--input', type=str, required=True, help="Path to the input code file.")
    parser.add_argument('--output', type=str, required=True, help="Path to save the preprocessed code.")
    parser.add_argument('--language', type=str, default='Python', help="Programming language of the code (default: Python).")
    args = parser.parse_args()

    try:
        preprocessed_code = preprocess_code(args.input, args.language)  # Preprocess input code
        save_preprocessed_code(args.output, preprocessed_code)  # Save processed code
        print("Code preprocessing completed successfully.")
    except Exception as e:
        print(f"Error: {e}")  # Handle errors and exceptions
