#¡/usr/bin/env python3
#
# Split a Python file full of classes into a module.

import inflection
import os
import re
import sys

pattern = re.compile(r'^class\s+(\w*)')

def munge(fn):
    if not fn.endswith('.py'):
        raise Exception("Must supply a .py file as argument")
    d = os.path.splitext(fn)[0]
    if os.path.exists(d):
        raise Exception(f"{d} already exists - not overwriting")
    os.mkdir(d)
        
    imports = []
    with open(fn) as f:
        for line in f.readlines():
            if (line.startswith('from ') and ' import ' in line) or line.startswith('import'):
                if line.startswith('from .'):
                    line = 'from ' + '.'.join(os.path.split(d)[:-1]) + line[5:]
                imports.append(line)
                
    
    with open(os.path.join(d, '__init__.py'), 'w') as init:
        with open(fn) as f:
            current_class_file = None
            for line in f.readlines():
                if line.startswith('class '):
                    match = pattern.match(line)
                    if match:
                        class_name = match.groups()[0]
                        us_class_name = inflection.underscore(class_name)
                        if current_class_file is not None:
                            current_class_file.close()
                        current_class_file = open(os.path.join(d, f"{us_class_name}.py"), 'w')
                        current_class_file.write(''.join(imports))
                        current_class_file.write('\n')
                        init.write(f"from .{us_class_name} import {class_name}\n")
                if current_class_file is not None:
                    current_class_file.write(line)
    current_class_file.close()
    
if __name__ == '__main__':
    munge(sys.argv[1])

            