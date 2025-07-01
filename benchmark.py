import subprocess  # Allows running shell commands and external processes
import time  # Used to measure execution time
import os  # Provides functions to interact with the operating system

def execute_code(file_path, language='Python'):
    """
    Executes the given code file and measures its runtime.
    Supports Python and C languages.
    Returns the execution time in seconds.
    """
    start_time = time.time()  # Record the start time of execution
    try:
        if language == 'Python':
            # Execute Python script using the Python interpreter
            subprocess.run(["python", file_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif language == 'C':
            # Compile and execute C code
            executable = file_path.replace('.c', '')  # Generate the output executable filename
            subprocess.run(["gcc", file_path, "-o", executable], check=True)  # Compile C code
            subprocess.run([f"./{executable}"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Run compiled C program
        else:
            raise ValueError(f"Unsupported language: {language}")  # Raise an error for unsupported languages
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error while executing code: {e.stderr.decode()}")  # Handle execution errors
    finally:
        end_time = time.time()  # Record the end time after execution
        execution_time = end_time - start_time  # Calculate total execution time
    return execution_time  # Return execution time in seconds

def benchmark_performance(original_code_path, optimized_code, language='Python'):
    """
    Benchmarks the performance of original and optimized code.
    Steps:
    1. Save the optimized code in a temporary file.
    2. Execute both versions and measure their execution time.
    3. Compare performance improvement.
    """
    print("Benchmarking performance...")
    optimized_code_path = "temp_optimized_code" + (".py" if language == 'Python' else ".c")  # Create a temporary file for the optimized code
    
    # Save the optimized code to the temporary file
    with open(optimized_code_path, 'w') as file:
        file.write(optimized_code)
    
    # Measure runtime of the original code
    print("Running original code...")
    original_time = execute_code(original_code_path, language)  # Execute the original code
    print(f"Original Code Execution Time: {original_time:.4f} seconds")

    # Measure runtime of the optimized code
    print("Running optimized code...")
    optimized_time = execute_code(optimized_code_path, language)  # Execute the optimized code
    print(f"Optimized Code Execution Time: {optimized_time:.4f} seconds")
    
    # Remove the temporary optimized file after execution
    if os.path.exists(optimized_code_path):
        os.remove(optimized_code_path)
    
    # Calculate performance improvement percentage
    performance_gain = ((original_time - optimized_time) / original_time) * 100 if original_time > 0 else 0
    print(f"Performance Improvement: {performance_gain:.2f}%")
    
    # Return benchmark results in a dictionary format
    return {
        "original_time": original_time,
        "optimized_time": optimized_time,
        "performance_gain": performance_gain
    }

if __name__ == '__main__':
    import argparse  # Used to parse command-line arguments
    from preprocess import load_code  # Import function to load optimized code from a file
    
    # Setup argument parser to accept command-line inputs
    parser = argparse.ArgumentParser(description="Benchmark runtime performance of code.")
    parser.add_argument('--input', type=str, required=True, help="Path to the original code file.")
    parser.add_argument('--optimized', type=str, required=True, help="Path to the optimized code content file.")
    parser.add_argument('--language', type=str, default='Python', help="Programming language (default: Python).")
    args = parser.parse_args()  # Parse the provided command-line arguments
    
    try:
        # Load the optimized code content from the specified file
        optimized_code = load_code(args.optimized)
        
        # Run the benchmarking process for both versions
        metrics = benchmark_performance(args.input, optimized_code, args.language)
        
        # Display the benchmark results
        print("Benchmark Results:")
        print(f"Original Time: {metrics['original_time']:.4f} seconds")
        print(f"Optimized Time: {metrics['optimized_time']:.4f} seconds")
        print(f"Performance Improvement: {metrics['performance_gain']:.2f}%")
    except Exception as e:
        print(f"Error: {e}")  # Print any error that occurs during execution
