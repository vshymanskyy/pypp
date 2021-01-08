#!/usr/bin/env pypp
#delim("py:", "%{", "}%")

# Let's generate some Python code!

py:GREETING = "Hello {n}!"

n = "PYPP"

print(f"%{GREETING}%")

py:begin
for x in range(10):
    print(f'print("wow {x}")');
py:end
