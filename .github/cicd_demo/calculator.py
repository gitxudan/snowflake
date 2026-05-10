def addition(x:int, y:int) -> int:
    return x + y

def subtraction(x:int, y:int) -> int:
    return x - y

def multiplication(x:int, y:int) -> int:
    return x * y

def division(x:int, y:int) -> float:
    if y == 0:
        raise ValueError("Denominator cannot be zero.")
    return x / y    