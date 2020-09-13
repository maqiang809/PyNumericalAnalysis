def checkEqual(i, j, message="Dimension Dismatch!"):
    if (i != j):
        raise ValueError(message)

def checkRange(idx, low, upp, message="Index Out of Bounds"):
    if idx < low or idx >= upp:
        raise ValueError(message)

def checkPositive(x, message = "value must be positive"):
    if (x < 0):
        raise ValueError(message)