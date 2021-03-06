#from pypp.lang.wasm import *   # use WebAssembly helpers
#replace(";;.*?\n","\n")        # remove comments

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
