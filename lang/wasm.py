import struct, binascii

'''
  Functions to generate raw(hex) data for built-in types
  This is similar to wat-numeric-values WebAssembly proposal:
    https://github.com/WebAssembly/wat-numeric-values
'''

def hexdata(fmt):
    def func(*args):
        data = [struct.pack('<'+fmt, x) for x in args]
        data = ['"\\'+ binascii.hexlify(x, '\\').decode() + '"' for x in data]
        return ' '.join(data)
    return func

i8  = hexdata('B')
i16 = hexdata('H')
i32 = hexdata('I')
i64 = hexdata('Q')
f32 = hexdata('f')
f64 = hexdata('d')
