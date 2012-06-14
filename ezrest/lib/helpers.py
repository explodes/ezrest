
def first(*args):
    func, sequence = args
    if sequence:
        if func:
            for x in sequence:
                if func(x):
                    return x
        else:
            return sequence[0]
