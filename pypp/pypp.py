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

    if sandbox == None:
        sandbox = {}
        sandbox["defined"] = lambda name: name in sandbox
        sandbox["__process"] = process
        sandbox["__pypp"] = dotdict({
            "stack": []
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

__postproc = []
__preproc = []

def include(s):
    (path, _) = os.path.split(__pypp.stack[-1])
    __process(os.path.join(path, s), globals())

def replace(a,b):
    __preproc.append(lambda s: re.sub(a, b, s))
    
def __emit(s):
    for func in __preproc:
        s = func(s)
    exec(f'__res = f\"\"\"{s}\"\"\"', globals())
    s = __res
    for func in __postproc:
        s = func(s)
    print(s)
"""

    #process text

    code_block = False
    with open(fn, 'r') as f:
        for sep, group in itertools.groupby(f, lambda l: l.startswith("#")):
            group = list(group)
            #print(sep, group)
            if sep:
                for block in group:
                    if block.startswith("#begin"):
                        if code_block:
                            raise Exception("#begin inside code block")
                        code_block = True
                    elif block.startswith("#end"):
                        if not code_block:
                            raise Exception("#end should come after a matching #begin")
                        code_block = False
                    else:
                        pycode += block[1:]
            else:
                block = "".join(group)
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
