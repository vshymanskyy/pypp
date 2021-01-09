
import re
import os
from pypp.lang.common import *

__preproc = [
    lambda s: s.replace(__pypp.delims[0], '\x04'),
    lambda s: s.replace(__pypp.delims[1], '\x05'),
    lambda s: s.replace('{', '\x02'),
    lambda s: s.replace('}', '\x03'),
    lambda s: s.replace('\x04', '{'),
    lambda s: s.replace('\x05', '}'),
]

__postproc = [
    lambda s: s.replace('\x02', '{'),
    lambda s: s.replace('\x03', '}'),
]

def include(s):
    (path, _) = os.path.split(__pypp.stack[-1])
    __pypp.process(os.path.join(path, s), globals())

def replace(a,b):
    __preproc.append(lambda s: re.sub(a, b, s))
    
def __emit(s):
    for func in __preproc:
        s = func(s)
    exec(f'__res = f"""{s}"""', globals())
    s = __res
    for func in __postproc:
        s = func(s)
    print(s, end='')
__pypp.delims[0]='%{'
__pypp.delims[1]='}%'
__emit(r"""
# Let's generate some Python code!

""")
GREETING = "Hello {n}!"
__emit(r"""
n = "PYPP"

print(f"%{GREETING}%")

""")
for x in range(10):
    print(f'print("wow {x}")');

