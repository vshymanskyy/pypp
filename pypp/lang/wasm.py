import struct, binascii

'''
  Functions to generate raw(hex) data for built-in types
  This is similar to wat-numeric-values WebAssembly proposal:
    https://github.com/WebAssembly/wat-numeric-values
'''

def hexstr(buff):
    s = binascii.hexlify(buff).decode()
    return '"\\'+ '\\'.join([s[i:i+2] for i in range(0, len(s), 2)]) + '"'

def hexdata(fmt):
    def func(*args):
        data = [struct.pack('<'+fmt, x) for x in args]
        return ' '.join([hexstr(x) for x in data])
    return func

i8  = hexdata('B')
i16 = hexdata('H')
i32 = hexdata('I')
i64 = hexdata('Q')
f32 = hexdata('f')
f64 = hexdata('d')
