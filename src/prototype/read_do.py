import os
import re
import sys

class StataCodeAnalyzer:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.do_files = []
        self.global_macros = {}
        self.dependencies = {}

    def find_do_files(self):
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.do'):
                    self.do_files.append(os.path.join(root, file))

    def parse_do_files(self):
        for do_file in self.do_files:
            with open(do_file, 'r') as f:
                content = f.read()
                self.parse_global_macros(content)
                self.parse_dependencies(do_file, content)

    def parse_global_macros(self, content):
        global_macro_pattern = r'global\s+(\w+)\s+(.+)'
        matches = re.findall(global_macro_pattern, content)
        for match in matches:
            self.global_macros[match[0]] = match[1].strip()

    def parse_dependencies(self, do_file, content):
        self.dependencies[do_file] = {
            'inputs': set(),
            'outputs': set(),
            'macros': set()
        }

        # Parse dataset inputs
        input_pattern = r'use\s+(.+?)(?:,|\s|$)'
        inputs = re.findall(input_pattern, content)
        self.dependencies[do_file]['inputs'].update(inputs)

        # Parse dataset outputs
        output_pattern = r'save\s+(.+?)(?:,|\s|$)'
        outputs = re.findall(output_pattern, content)
        self.dependencies[do_file]['outputs'].update(outputs)

        # Parse macro usage
        macro_pattern = r'\$(\w+)'
        macros = re.findall(macro_pattern, content)
        self.dependencies[do_file]['macros'].update(macros)

        # Parse local macros (simplified, doesn't handle nested locals)
        local_pattern = r'local\s+(\w+)\s+(.+)'
        local_matches = re.findall(local_pattern, content)
        for match in local_matches:
            self.dependencies[do_file]['macros'].add(match[0])

        # TODO: Add parsing for loops (for and foreach)

    def analyze(self):
        self.find_do_files()
        self.parse_do_files()

    def print_results(self):
        print("Do Files:")
        for file in self.do_files:
            print(f"{file}")

        print("Global Macros:")
        for macro, value in self.global_macros.items():
            print(f"  {macro}: {value}")

        print("\nDependencies:")
        for do_file, deps in self.dependencies.items():
            print(f"\n{do_file}:")
            print("  Inputs:")
            for input_file in deps['inputs']:
                print(f"    {input_file}")
            print("  Outputs:")
            for output_file in deps['outputs']:
                print(f"    {output_file}")
            print("  Macros Used:")
            for macro in deps['macros']:
                print(f"    {macro}")

if __name__ == "__main__":
    path = sys.argv[1]
    root_directory = f"{path}"
    analyzer = StataCodeAnalyzer(root_directory)
    analyzer.analyze()
    analyzer.print_results()