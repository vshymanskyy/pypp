#delim("py:", "%{", "}%")

#include <iostream>

py:GREETING = "Hello PYPP!"

int main() {
    std::cout << %{GREETING}% << "\n";
py:begin
for x in range(10):
    print(f'std::cout << "{x}";')
py:end
    return 0;
}
