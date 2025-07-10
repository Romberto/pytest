from typing import Union


class Calculator:

    def devide(self, x: Union[int | float], y: Union[int | float]) -> int | float:
        if not isinstance(x, (int| float)) or not isinstance(y, (int | float)):
            raise TypeError("не правельный формат данных")
        if y == 0:
            raise ZeroDivisionError("на ноль делить нельзя")
        return x / y

    def add(self, x: Union[int | float], y: Union[int | float]) -> int | float:
        if not isinstance(x, (int| float)) or not isinstance(y, (int | float)):
            raise TypeError("не правельный формат данных")
        return x + y



if __name__ == '__main__':
    calculator = Calculator()
