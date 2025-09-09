import ast

def analyze_python_code(code_string):
    """
    Analyzes a Python code string for unused variables and parameters using the ast module.
    """
    issues = []

    try:
        # Parse the code into an Abstract Syntax Tree
        tree = ast.parse(code_string)
        
        # Traverse the AST to find function definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                
                # Find all declared variables and parameters
                all_declared = set()
                
                # Add function parameters
                for arg in node.args.args:
                    all_declared.add(arg.arg)
                
                # Find all used variables
                all_used = set()
                
                for sub_node in ast.walk(node):
                    if isinstance(sub_node, ast.Name) and isinstance(sub_node.ctx, ast.Load):
                        all_used.add(sub_node.id)

                    # Also check for assigned variables that are unused
                    if isinstance(sub_node, ast.Assign):
                        for target in sub_node.targets:
                            if isinstance(target, ast.Name):
                                # An assigned variable that is not a parameter is a local variable
                                if target.id not in [arg.arg for arg in node.args.args]:
                                    all_declared.add(target.id)

                # Identify unused parameters/variables
                for var in all_declared:
                    if var not in all_used:
                        issues.append(f"Issue: Unused variable/parameter '{var}' in function '{function_name}'")

        if not issues:
            return "No issues found."
        
        return "\n".join(issues)

    except SyntaxError as e:
        return f"Syntax Error: {e}"
    except Exception as e:
        return f"Error during Python analysis: {e}"

# Simple test cases for the updated analyzer
if __name__ == "__main__":
    test_code_1 = """
def add_numbers(x, y):
    result = x + 10
    return result
"""
    print("--- Test Case 1 ---")
    print(analyze_python_code(test_code_1))

    test_code_2 = """
def my_function():
    a = 10
    b = 20
    print(b)
"""
    print("\n--- Test Case 2 ---")
    print(analyze_python_code(test_code_2))