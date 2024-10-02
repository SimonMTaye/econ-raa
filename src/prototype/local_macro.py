import re
from typing import List, Optional, Union, Dict, Any

class MacroDefinition:
    def __init__(self, name: str):
        self.name = name
        self.values: List[Union[str, Dict[str, Any]]] = []

    def add_value(self, value: Union[str, Dict[str, Any]]):
        self.values.append(value)

class StataMacroExpander:
    def __init__(self, do_file_path: str):
        self.do_file_path = do_file_path
        self.macros: Dict[str, MacroDefinition] = {}
        self.parse_do_file()

    def parse_do_file(self):
        with open(self.do_file_path, 'r') as file:
            content = file.read()

        # Split the content into blocks (separated by newlines)
        blocks = re.split(r'\n\s*\n', content)

        for block in blocks:
            self.parse_block(block)

    def parse_block(self, block: str):
        # Parse if-else structures
        if_else_pattern = r'if\s+(.+?)\s*{(.+?)}\s*(?:else\s*{(.+?)})?'
        if_else_match = re.search(if_else_pattern, block, re.DOTALL)
        
        if if_else_match:
            condition, if_block, else_block = if_else_match.groups()
            self.parse_conditional_block(if_block, condition)
            if else_block:
                self.parse_conditional_block(else_block, f"not ({condition})")
        else:
            self.parse_simple_block(block)

    def parse_conditional_block(self, block: str, condition: str):
        lines = block.strip().split('\n')
        for line in lines:
            match = re.match(r'local\s+(\w+)(?:\s+(.+))?', line.strip())
            if match:
                macro_name, macro_value = match.groups()
                if macro_name not in self.macros:
                    self.macros[macro_name] = MacroDefinition(macro_name)
                self.macros[macro_name].add_value({
                    "condition": condition,
                    "value": macro_value if macro_value else None
                })

    def parse_simple_block(self, block: str):
        # Parse local macro definitions
        local_pattern = r'local\s+(\w+)(?:\s+(.+?))?(?:\n|$)'
        for match in re.finditer(local_pattern, block):
            macro_name, macro_value = match.groups()
            if macro_name not in self.macros:
                self.macros[macro_name] = MacroDefinition(macro_name)
            self.macros[macro_name].add_value(macro_value if macro_value else None)

        # Parse forvalues loops
        forvalues_pattern = r'forvalues\s+(\w+)\s*=\s*(.+?)\s*{(.+?)}'
        for match in re.finditer(forvalues_pattern, block, re.DOTALL):
            macro_name, range_spec, _ = match.groups()
            if macro_name not in self.macros:
                self.macros[macro_name] = MacroDefinition(macro_name)
            self.macros[macro_name].add_value(f"forvalues:{range_spec}")

        # Parse foreach loops
        foreach_pattern = r'foreach\s+(\w+)\s+(?:of|in)\s+(.+?)\s*{(.+?)}'
        for match in re.finditer(foreach_pattern, block, re.DOTALL):
            macro_name, items, _ = match.groups()
            if macro_name not in self.macros:
                self.macros[macro_name] = MacroDefinition(macro_name)
            self.macros[macro_name].add_value(f"foreach:{items}")

    def get_macro_values(self, macro_name: str) -> List[Any]:
        if macro_name not in self.macros:
            return []

        macro_def = self.macros[macro_name]
        results = []

        for value in macro_def.values:
            if isinstance(value, dict):
                # Conditional value
                results.append(f"If {value['condition']}: {self.expand_value(value['value'])}")
            else:
                results.extend(self.expand_value(value))

        return results

    def expand_value(self, value: Optional[str]) -> List[Any]:
        if value is None:
            return [None]
        elif value.startswith("forvalues:"):
            return self._expand_forvalues(value[10:])
        elif value.startswith("foreach:"):
            return self._expand_foreach(value[8:])
        else:
            # Handle nested macro references
            expanded = re.sub(r'`(\w+)\'', lambda m: self.expand_nested_macro(m.group(1)), value)
            return [expanded]

    def expand_nested_macro(self, macro_name: str) -> str:
        values = self.get_macro_values(macro_name)
        if not values:
            return f"`{macro_name}'"
        elif len(values) == 1:
            return str(values[0])
        else:
            return f"[{', '.join(map(str, values))}]"

    def _expand_forvalues(self, range_spec: str) -> List[int]:
        if '/' in range_spec:
            start, end = map(int, range_spec.split('/'))
            return list(range(start, end + 1))
        elif 'to' in range_spec:
            start, end = map(int, range_spec.split('to'))
            return list(range(start, end + 1))
        else:
            return [int(range_spec)]

    def _expand_foreach(self, items: str) -> List[str]:
        if items.startswith('"') and items.endswith('"'):
            # List of space-separated items
            return items[1:-1].split()
        elif items.startswith('`') and items.endswith("'"):
            # Macro expansion
            return self.get_macro_values(items[1:-1])
        else:
            # Assume it's a list of variables or similar
            return items.split()

def main(do_file_path: str):
    expander = StataMacroExpander(do_file_path)
    
    print(f"Macros found in {do_file_path}:")
    for macro_name in expander.macros:
        values = expander.get_macro_values(macro_name)
        print(f"{macro_name}: {values}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_do_file>")
        sys.exit(1)
    main(sys.argv[1])