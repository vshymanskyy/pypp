import sys

class ListStream:
    def __init__(self):
        self.data = []
    def write(self, s):
        self.data.append(s)
    def get_data(self):
        return "".join(self.data)
    def __enter__(self):
        sys.stdout = self
        return self
    def __exit__(self, ext_type, exc_value, traceback):
        sys.stdout = sys.__stdout__  

from pypp import pypp
import random as rand

def check_py(fn):
    rand.seed(0)        # reproducible random

    with open(f'./test/expected_{fn}.py', 'r') as f:
        expected = f.read()

    with ListStream() as out:
        pypp.process(f'./examples/{fn}', None, True)
        actual = out.get_data()

    assert(actual == expected)
    
def check_final(fn):
    rand.seed(0)        # reproducible random

    with open(f'./test/expected_{fn}', 'r') as f:
        expected = f.read()

    with ListStream() as out:
        pypp.process(f'./examples/{fn}')
        actual = out.get_data()

    assert(actual == expected)
    
# Python generation tests

def test_webasm_py():
    check_py('webassembly.wat')

def test_webpage_py():
    check_py('webpage.html')
    
def test_python_py():
    check_py('python.py')

def test_cplusplus_py():
    check_py('cplusplus.cpp')

# Final result tests

def test_webpage():
    check_final('webpage.html')

def test_python():
    check_final('python.py')

def test_cplusplus():
    check_final('cplusplus.cpp')
