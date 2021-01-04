#!/usr/bin/env python3

import itertools
import re
import os

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def process(path, fn, sandbox = {}):
    # reassemble path and fn
    full_fn = os.path.join(path, fn)
    (path, fn) = os.path.split(full_fn)

    preprocessors = []
    
    # directives
    
    def _import(s):     exec(f"from {s} import *", sandbox)
    def _include(s):    process(path, s, sandbox.copy())
    def _replace(a,b):  preprocessors.append(lambda s: re.sub(a, b, s))

    # initialize sandbox

    sandbox["__pypp_d"] = dotdict({
        "_import":      _import,
        "_include":     _include,
        "_replace":     _replace,
    })
    sandbox["defined"] = lambda name: name in sandbox

    exec("import lang.common", sandbox)

    #process text

    code_block = False
    with open(full_fn, 'r') as f:
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
                    elif block.startswith("#import") or block.startswith("#include") or block.startswith("#replace"):
                        exec(f"__pypp_d._{block[1:]}", sandbox)
            else:
                block = "".join(group)
                if code_block:
                    #print("CODE:", group)
                    exec(block, sandbox)
                else:
                    #print("TEXT:", group)
                    block = block.replace('\\', '\\\\')
                    
                    for pre in preprocessors:
                        block = pre(block)
                        
                    exec(f'__res = f"""{block}"""', sandbox)
                    print(sandbox["__res"], end='')
                    del sandbox["__res"]

