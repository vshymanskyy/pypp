
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
    exec(f'__res = f"""{s}"""', globals())
    s = __res
    for func in __postproc:
        s = func(s)
    print(s, end='')
__preproc.append(lambda s: s.replace('%{', '\x04'))
__preproc.append(lambda s: s.replace('}%', '\x05'))
__preproc.append(lambda s: s.replace('{', '\x02'))
__preproc.append(lambda s: s.replace('}', '\x03'))
__preproc.append(lambda s: s.replace('\x04', '{'))
__preproc.append(lambda s: s.replace('\x05', '}'))
__postproc.append(lambda s: s.replace('\x02', '{'))
__postproc.append(lambda s: s.replace('\x03', '}'))
__emit(r"""
#include <iostream>

""")
GREETING = "Hello PYPP!"
__emit(r"""
int main() {
    std::cout << %{GREETING}% << "\\n";
""")
for x in range(10):
    print(f'std::cout << "{x}";')
__emit(r"""    return 0;
}
""")

