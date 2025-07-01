import argparse  # Library for parsing command-line arguments
import os  # Operating system functions for file handling
from preprocess import preprocess_code  # Import preprocessing function
from ml_optimizer import CodeOptimizerDQL  # Import machine learning optimizer
from benchmark import benchmark_performance  # Import benchmarking function

def main():
    """
    Main function for the RefineML - Intelligent Code Optimization Platform.
    Steps:
        1. Parse input arguments.
        2. Preprocess the input code.
        3. Optimize the code using DQL-based optimizer.
        4. Save the optimized code.
        5. Benchmark and compare performance.
    """
    parser = argparse.ArgumentParser(description="RefineML - Intelligent Code Optimization Platform")
    parser.add_argument('--input', type=str, required=True, help="Path to the input code file.")
    parser.add_argument('--language', type=str, default='Python', help="Programming language of the code (default: Python).")
    parser.add_argument('--output', type=str, required=True, help="Path to save the optimized code file.")

    args = parser.parse_args()

    # Check if the input file exists
    if not os.path.exists(args.input):
        print(f"[ERROR] File {args.input} does not exist.")
        return

    try:
        # Step 1: Preprocess the input code
        print("[INFO] Preprocessing code...")
        preprocessed_code = preprocess_code(args.input, args.language)
        print("[INFO] Code preprocessing completed.")

        # Step 2: Initialize the optimizer and optimize the code
        print("[INFO] Initializing optimizer...")
        optimizer = CodeOptimizerDQL(language=args.language)
        suggestions, optimized_code = optimizer.optimize_code(preprocessed_code)
        print("[INFO] Code optimization completed.")

        # Step 3: Save the optimized code
        with open(args.output, 'w') as output_file:
            output_file.write(optimized_code)
        print(f"[INFO] Optimized code saved to: {args.output}")

        # Step 4: Print optimization suggestions
        print("\n=== Optimization Suggestions ===")
        for suggestion in suggestions:
            print(f"- {suggestion}")

        # Step 5: Benchmark the performance
        print("\n=== Benchmark Results ===")
        benchmark_results = benchmark_performance(args.input, optimized_code, args.language)
        print(f"Original Execution Time: {benchmark_results['original_time']:.4f} seconds")
        print(f"Optimized Execution Time: {benchmark_results['optimized_time']:.4f} seconds")
        print(f"Performance Improvement: {benchmark_results['performance_gain']:.2f}%")

    except Exception as e:
        print(f"[ERROR] {e}")  # Handle exceptions

if __name__ == '__main__':
    main()
