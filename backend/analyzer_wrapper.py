import sys
import subprocess
import os
import tempfile
from python_analyzer import analyze_python_code  # Import the new analyzer

def analyze_code(code_string, language):
    """
    Analyzes a code string based on the specified language.

    Args:
        code_string (str): The code to analyze.
        language (str): The programming language ('cpp' or 'python').

    Returns:
        str: The analysis report.
    """
    if language == 'cpp':
        # Handle C++ analysis
        try:
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.cpp', encoding='utf-8') as temp_file:
                temp_file.write(code_string)
                temp_file_path = temp_file.name

            analyzer_path = os.path.join(os.path.dirname(__file__), '../analyzer_cpp/analyzer')

            process = subprocess.run(
                [analyzer_path, temp_file_path],
                capture_output=True,
                text=True,
                check=True
            )
            return process.stdout

        except FileNotFoundError:
            return "Error: The C++ analyzer executable was not found. Please ensure it is compiled and located at '../analyzer_cpp/analyzer'."
        except subprocess.CalledProcessError as e:
            return f"Error during analysis: {e.stderr}"
        finally:
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    elif language == 'python':
        # Handle Python analysis
        return analyze_python_code(code_string)

    else:
        return "Error: Unsupported language."

# A simple test case to demonstrate functionality
if __name__ == "__main__":
    print("--- Testing C++ Analyzer ---")
    sample_cpp_code = """
    #include <iostream>
    int main() {
        int x = 5;
        int y = 10;
        std::cout << y << std::endl;
        return 0;
    }
    """
    cpp_report = analyze_code(sample_cpp_code, 'cpp')
    print(cpp_report)

    print("--- Testing Python Analyzer ---")
    sample_python_code = """
    def my_function():
        x = 10
        y = 20
        print(y)
    """
    python_report = analyze_code(sample_python_code, 'python')
    print(python_report)