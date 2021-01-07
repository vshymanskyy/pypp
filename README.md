# PYPP - Python PreProcessor

**PYPP** formats the whole file using `f-string` syntax, with some additional helper directives and functions.  
It should be able to process any text: source code, config files, docs, etc. (after `custom delimiters` are implemented).

## Install

```sh
pip3 install https://github.com/vshymanskyy/pypp/archive/main.zip
```

## Usage example

Python 3 can be directly used to generate other files:

```py
from random import randrange

TITLE = "Hello"

print(f"""<!DOCTYPE html>
<html><body>
  <h1>{TITLE}</h1>
  <ul>
  <!-- Some random numbers! -->
""")
for i in range(5):
    print(f"<li>{randrange(1,100)}</li>", end="")
print(f"""
  </ul>
</body></html>
""")
```

It turns out to be very flexible, but there are several problems with this approach:  
Unreadable, too much boilerplate. Characters like `{}\` need to be manually escaped in `f-strings`, so it's unusable for processing `C/C++`, `Java`, `JS/JSON`, `Python` files. Python code draws a lot of attention, but it should be secondary here. If you want to include other files it becomes even more unreadable, etc.

PYPP is based on the same idea, but it tries to solve the above issues.

This is an equivalent PYPP template:
```py
#TITLE = "Hello PYPP"
<!DOCTYPE html>
<html><body>
  <h1>{TITLE}</h1>
  <ul>
  <!-- Some random numbers! -->
#begin
from random import randrange
for i in range(5):
    print(f"<li>{randrange(1,100)}</li>", end='')
print()
#end
  </ul>
</body></html>
```

After running `pypp template.html > result.html`, you get: 

```html
<!DOCTYPE html>
<html><body>
  <h1>Hello PYPP</h1>
  <ul>
  <!-- Some random numbers! -->
<li>8</li><li>15</li><li>33</li><li>85</li><li>38</li>
  </ul>
</body></html>
```

**WebAssembly**

Template:
```wasm
#from pypp.lang.wasm import *   # use WebAssembly helpers
#replace(';;.*?\n','\n')        # remove comments

#ANSWER = 40

(module
  (memory (export "mem") 1)
  (data (i32.const 0x0000)
    "\DE\AD\BE\EF"
    ;; Generate binary data for a float number
    ;; Similar to wat-numeric-values WebAssembly proposal
    {f32(3.14159265359)}
  )
  (func (export "question") (result i32)
    ;; Use math expression to adjust the answer
    (i32.const {ANSWER+2})
  )
)
```

Result:
```wasm
(module
  (memory (export "mem") 1)
  (data (i32.const 0x0000)
    "\DE\AD\BE\EF"
    "\db\0f\49\40"
  )
  (func (export "question") (result i32)
    (i32.const 42)
  )
)
```

## Directives

### `#include(<expr>)`
Include (and expand) another template file.  
Any Python expression can be used as an argument, like: `'utils.wat'`, `f'{HEADER}.html'`, etc.

### `#begin`..`#end`
Run arbitrary Python code.

### `#replace(<regex>, <string>)`
Replace arbitrary text.

## Ideas (not implemented!)

### `#delim('<%', '%>')`
Set custom delimiters.

### `#if(<expr>)`..`#elif(<expr>)`..`#else`..`#end`
Conditional block output.

### `#run_with(f'command {file} {args}'`)
Store output to a temporary file, and execute command automatically.
In conjunction with `#!/usr/bin/env pypp`, this should allow preprocessing and executing any templates as ordinary scripts.

__________

## License
This project is released under The MIT License (MIT)
