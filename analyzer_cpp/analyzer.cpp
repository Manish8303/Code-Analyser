#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <regex>

// Function to trim leading and trailing whitespace from a string
std::string trim(const std::string& str) {
    size_t first = str.find_first_not_of(" \t\n\r");
    if (std::string::npos == first) {
        return str;
    }
    size_t last = str.find_last_not_of(" \t\n\r");
    return str.substr(first, (last - first + 1));
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <source_file>" << std::endl;
        return 1;
    }

    std::ifstream file(argv[1]);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << argv[1] << std::endl;
        return 1;
    }

    std::string line;
    std::unordered_map<std::string, int> declared_vars;
    std::unordered_map<std::string, int> used_vars;
    int line_number = 0;

    // A more robust regex to find variable declarations
    std::regex var_decl_regex(R"((?:int|char|long|float|double|bool|string)\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\s*=|;|,))");

    std::vector<std::string> lines;
    while (getline(file, line)) {
        lines.push_back(line);
    }
    file.close();

    // Pass 1: Find all declared variables
    line_number = 0;
    for (const auto& l : lines) {
        line_number++;
        std::smatch match;
        if (std::regex_search(l, match, var_decl_regex)) {
            std::string var_name = match[1].str();
            declared_vars[var_name] = line_number;
        }
    }

    // Pass 2: Check for variable usage
    for (const auto& l : lines) {
        for (const auto& pair : declared_vars) {
            // Check if the variable is used in the line
            if (l.find(pair.first) != std::string::npos) {
                // Ensure the variable is not just part of a declaration again
                // This is a simplified check
                size_t decl_pos = l.find(pair.first);
                if (decl_pos != std::string::npos) {
                    bool is_in_declaration = false;
                    for (const auto& decl_type : {"int", "char", "long", "float", "double", "bool", "string"}) {
                        if (l.find(std::string(decl_type) + " " + pair.first) != std::string::npos) {
                            is_in_declaration = true;
                            break;
                        }
                    }
                    if (!is_in_declaration) {
                        used_vars[pair.first]++;
                    }
                }
            }
        }
    }

    // Report unused variables
    bool found_issues = false;
    std::cout << "--- Code Analysis Report ---" << std::endl;

    for (const auto& pair : declared_vars) {
        std::string var_name = pair.first;
        // If the variable is used only in its declaration (count will be 0)
        if (used_vars.find(var_name) == used_vars.end()) {
            std::cout << "Issue: Unused variable '" << var_name << "' at line " << declared_vars[var_name] << std::endl;
            found_issues = true;
        }
    }

    if (!found_issues) {
        std::cout << "No issues found." << std::endl;
    }

    std::cout << "--- End of Report ---" << std::endl;

    return 0;
}