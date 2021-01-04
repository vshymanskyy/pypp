#!/usr/bin/env python3

import itertools
import re
import os

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

sandbox = {
    "defined": lambda name: name in sandbox,
}

preprocessors = []

def expr(s):
    exec(f'__res = {s}', sandbox)
    r = sandbox["__res"]
    del sandbox["__res"]
    return r

def process_code(s):
    exec(s, sandbox)
    
def process_text(s):
    s = s.replace('\\', '\\\\')
    
    for pre in preprocessors:
        s = pre(s)
    print(expr(f'f"""{s}"""'), end='')

def process(path, fn):
    # reassemble path and fn
    full_fn = os.path.join(path, fn)
    (path, fn) = os.path.split(full_fn)

    code_block = False
    
    def _import(s):     exec(f"from {s} import *", sandbox)
    def _include(s):    process(path, s)
    def _replace(a,b):  preprocessors.append(lambda s: re.sub(a, b, s))

    sandbox["__pypp_d"] = dotdict({
        "_import":      _import,
        "_include":     _include,
        "_replace":     _replace,
    })

    exec("import lang.common", sandbox)

    with open(full_fn, 'r') as f:
        for sep, group in itertools.groupby(f, lambda l: l.startswith("#")):
            group = list(group)
            #print(sep, group)
            if sep:
                for block in group:
                    if block.startswith("#begin"):
                        if code_block:
                            raise Exception("#begin 2nd time inside the same code block")
                        code_block = True
                    elif block.startswith("#end"):
                        if not code_block:
                            raise Exception("#end should come after a matching #begin")
                        code_block = False
                    elif block.startswith("#import") or block.startswith("#include") or block.startswith("#replace"):
                        exec(f"__pypp_d._{block[1:]}", sandbox)
            else:
                block = "".join(group)
                if code_block:
                    #print("CODE:", group)
                    process_code(block)
                else:
                    #print("TEXT:", group)
                    process_text(block)
