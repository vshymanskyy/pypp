#!/usr/bin/env python3

import itertools
import re
import os

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def process(fn, sandbox = None, emit_py = False):
    fn = os.path.relpath(fn)
    
    pydelim = '#'

    if sandbox == None:
        sandbox = {}
        sandbox["defined"] = lambda name: name in sandbox
        sandbox["__pypp"] = dotdict({
            "stack": [],
            "delims": ['{', '}'],
            "process": process,
        })
        
    __pypp = sandbox["__pypp"]
    
    # check for cyclic include
    __pypp.stack.append(fn)
    if any([os.path.samefile(fn, x) for x in __pypp.stack[:-1]]):
        raise Exception("Cyclic include:\n" + " ->\n".join(__pypp.stack))

    # generate Python code
    pycode = """
import re
import os
from pypp.lang.common import *

__preproc = [
    lambda s: s.replace(__pypp.delims[0], '\\x04'),
    lambda s: s.replace(__pypp.delims[1], '\\x05'),
    lambda s: s.replace('{', '\\x02'),
    lambda s: s.replace('}', '\\x03'),
    lambda s: s.replace('\\x04', '{'),
    lambda s: s.replace('\\x05', '}'),
]

__postproc = [
    lambda s: s.replace('\\x02', '{'),
    lambda s: s.replace('\\x03', '}'),
]

def include(s):
    (path, _) = os.path.split(__pypp.stack[-1])
    __pypp.process(os.path.join(path, s), globals())

def replace(a,b):
    __preproc.append(lambda s: re.sub(a, b, s))
    
def __emit(s):
    for func in __preproc:
        s = func(s)
    exec(f'__res = f\"\"\"{s}\"\"\"', globals())
    s = __res
    for func in __postproc:
        s = func(s)
    print(s, end='')
"""

    def delim(d, b='%{', e='}%'):
        nonlocal pycode, pydelim
        pydelim = d
        pycode += f"__pypp.delims[0]='{b}'\n"
        pycode += f"__pypp.delims[1]='{e}'\n"

    code_block = False
    with open(fn, 'r') as f:
        lines = f.read().splitlines(True)
        
        i = 0
        while i < len(lines):
            line = lines[i]
            if i < 10 and line.startswith("#!"):         # shebang
                i += 1
                continue
            if line.startswith(pydelim):
                line = line[len(pydelim):]
                if line.startswith("delim("):
                    exec(line, globals(), locals())

                elif line.startswith("begin"):
                    if code_block:
                        raise Exception("begin inside code block")
                    code_block = True
                elif line.startswith("end"):
                    if not code_block:
                        raise Exception("end should come after a matching begin")
                    code_block = False
                else:
                    pycode += line
                i += 1
            else:
                block = []
                while i < len(lines) and not lines[i].startswith(pydelim):
                    block.append(lines[i])
                    i += 1
                block = "".join(block)
                if code_block:
                    pycode += block
                else:
                    block = block.replace('\\', '\\\\')

                    if len(block.strip()):
                        pycode += f'__emit(r"""{block}""")\n'


        if emit_py:
            print(pycode)
        else:
            exec(pycode, sandbox.copy())
