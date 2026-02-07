import json
import os

class Reporter:
    def __init__(self):
        self.results = dict()

    def add_result(self, key: str, passed: bool, notes: str):
        self.results[key] = {
            "passed": passed,
            "notes": notes
        }
    
    def print_results(self, errors_only: bool = True, gha_commands = True):
        err_prefix = "::error::" if gha_commands else ""
        not_prefix = "::notice::" if gha_commands else ""
        err_suffix = "not valid"
        not_suffix = "valid"
        for key, result in self.results.items():
            if errors_only and result["passed"]:
                continue
            prefix = not_prefix if result["passed"] else err_prefix
            suffix = not_suffix if result["passed"] else err_suffix
            print(f"{prefix}{key}: {suffix}")
            print(result['notes'])
    
    def write_results(self, file_path: str, format: str):
        # Make sure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if format == "json":
            self.__write_json(file_path)
        elif format == "txt":
            self.__write_txt(file_path)
    
    def is_successful(self):
        return all(result["passed"] for result in self.results.values())
    
    def __write_json(self, file_path: str):
        with open(file_path, "w") as f:
            json.dump(self.results, f, indent=2)
    
    def __write_txt(self, file_path: str):
        with open(file_path, "w") as f:
            for key, result in self.results.items():
                f.write(f"{key}: {'valid' if result['passed'] else 'not valid'}\n")
                f.write(f"{result['notes']}\n\n")