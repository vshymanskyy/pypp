# PYPP - Python PreProcessor

**PYPP** formats the whole file using `f-string` syntax, with some additional helper directives and functions.  
It should be able to process any text: source code, config files, docs, etc. (after `custom delimiters` are implemented).

## Install

```sh
pip3 install https://github.com/vshymanskyy/pypp/archive/main.zip
```

## Usage example

**HTML**

Template:
```py
<!DOCTYPE html>
<html><body>
  <h1>Hello PYPP</h1>
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
#import('lang.wasm')        # Import WebAssembly helpers
#replace(';;.*?\n','\n')    # Remove comments

#begin
ANSWER = 40
#end

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

`TODO`

### `#include(<expr>)`
Include (and expand) another template file.  
Any Python expression can be used as an argument, like: `'utils.wat'`, `f'{HEADER}.html'`, etc.

### `#import(<expr>)`
Equivalent to:
```
#begin
from something import *
#end
```
It simplifies importing language-specific helper modules:
```
#import('lang.wasm')
```

### `#begin`..`#end`
Run arbitrary Python code

### `#replace(<regex>, <string>)`
Replace arbitrary text.

## Ideas (not implemented!)

### `#delim('<%', '%>')`
Set custom delimiters.

### `#run_with(f'command {file} {args}'`)
Store output to a temporary file, and execute command automatically.
When combined with `#!/usr/bin/env pypp`, this should allow preprocessing and executing any templates as ordinary scripts.

__________

## License
This project is released under The MIT License (MIT)
