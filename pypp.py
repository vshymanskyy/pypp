#!/usr/bin/env python3

import itertools

sandbox = {
    "defined": lambda name: name in sandbox
}

exec("import lang.common", sandbox)

def expr(s):
    exec(f'__res = {s}', sandbox)
    r = sandbox["__res"]
    del sandbox["__res"]
    return r

def process_code(s):
    exec(s, sandbox)
    
def process_text(s):
    #s = re.sub(';;.*?\n', '\n', s) # remove comments
    s = s.replace('\\', '\\\\')
    print(expr(f'f"""{s}"""'), end='')

def process_import(s):
    exec(f"from {expr(s)} import *", sandbox)

def process_include(s):
    process(expr(s))

def process(fn):
    code_block = False

    with open(fn, 'r') as f:
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
                    elif block.startswith("#import"):
                        process_import(block[7:])
                    elif block.startswith("#include"):
                        process_include(block[8:])
            else:
                block = "".join(group)
                if code_block:
                    #print("CODE:", group)
                    process_code(block)
                else:
                    #print("TEXT:", group)
                    process_text(block)
