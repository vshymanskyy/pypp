
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
    print(s)
from pypp.lang.wasm import *   # use WebAssembly helpers
replace(";;.*?\n","\n")        # remove comments
ANSWER = 40
__emit(r"""
(module
  (memory (export "mem") 1)
  (data (i32.const 0x0000)
    "\\DE\\AD\\BE\\EF"
    ;; Generate binary data for a float number
    ;; Similar to wat-numeric-values WebAssembly proposal
    {f32(3.14159265359)}
  )
  (func (export "question") (result i32)
    ;; Use math expression to adjust the answer
    (i32.const {ANSWER+2})
  )
)
""")

