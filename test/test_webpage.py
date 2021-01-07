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

def test_webasm_py():
    check_py('webassembly.wat')

def test_webpage_py():
    check_py('webpage.html')

def test_webpage_html():
    rand.seed(0)        # reproducible random

    with open('./test/expected_webpage.html', 'r') as f:
        expected = f.read()

    with ListStream() as out:
        pypp.process('./examples/webpage.html')
        actual = out.get_data()

    assert(actual == expected)
