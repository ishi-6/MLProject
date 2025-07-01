import ctypes
import os

# Load the shared library
lib_path = os.path.abspath("performance_module.so")
performance_lib = ctypes.CDLL(lib_path)

# Define the function signature for the C function
performance_lib.run_benchmark.argtypes = [ctypes.c_char_p]
performance_lib.run_benchmark.restype = ctypes.c_double

# Test the benchmark function
code_snippet = b"""
for (int i = 0; i < 100000; i++) {
    for (int j = 0; j < 1000; j++) {
        int x = i * j;
    }
}
"""

# Call the C function and print the result
execution_time = performance_lib.run_benchmark(code_snippet)
print(f"Execution time: {execution_time:.6f} seconds")
