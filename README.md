# PYPP - Python PreProcessor

## Install

```sh
pip3 install https://github.com/vshymanskyy/pypp/archive/main.zip
```

## Usage example

**HTML**

Template:
```python
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
;; Import WebAssembly helpers
#import "lang.wasm"

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

Result (comments removed manually):
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

### `#include <expr>`
Includes another template file (and expands it).
Any Python expression can be used as an argument, like: `'utils.wat'`, `f'{HEADER}.html'`, etc.

### `#import <expr>`
Equivalent to:
```
#begin
from something import *
#end
```
It simplifies importing language-specific helper modules:
```
#import "lang.wasm"
```

### `#begin`..`#end`
Runs arbitrary Python code

__________

## License
This project is released under The MIT License (MIT)
